import asyncio
import json
from datetime import datetime, date

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.dateparse import parse_datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage
from .tasks import send_delayed_message


class ChatConsumer(AsyncConsumer):

	async def websocket_connect(self, event):

		thread_id = self.scope['url_route']['kwargs']['thread_id']
		thread_obj = await self.get_thread(thread_id)
		chat_room = f"thread_{thread_id}"
		self.chat_room = chat_room

		await self.channel_layer.group_add(
			chat_room,
			self.channel_name
		)

		await self.send({"type": "websocket.accept"})

	async def websocket_receive(self, event):
		front_end_data = event.get('text', None)
		if front_end_data is not None:
			ws_recieved_data: dict = json.loads(front_end_data)

			current_thread_id = ws_recieved_data['current_thread_id']
			current_user_id = ws_recieved_data['current_user_id']
			current_user_username = ws_recieved_data['current_user_username']
			is_anonymous_message = ws_recieved_data['is_anonymous_message']
			chat_message = ws_recieved_data['message']
			is_delay = ws_recieved_data['is_delay']

			response = {
				'message': chat_message,
			}

			if is_anonymous_message == 'anonymous':
				response['current_user_username'] = 'Anonymous'
				user_obj = None
			else:
				response['current_user_username'] = current_user_username
				user_obj: User = await self.get_user(current_user_id)

			thread_obj: Thread = await self.get_thread(current_thread_id)

			if is_delay == 'delay':
				delay_date = ws_recieved_data['delay_date']
				delay_time = ws_recieved_data['delay_time']

				delay, future_timestamp = await self.get_seconds_until_future_datetime_point(delay_date,
					                                                       delay_time)
				
				response['timestamp'] = future_timestamp
				final_data_for_sending = {
					'type': 'chat_message',
					'text': json.dumps(response, cls=DjangoJSONEncoder)
				}

				task = send_delayed_message.apply_async(args=[
					self.chat_room,
					final_data_for_sending,
					{
						'thread_obj': thread_obj,
						'user_obj': user_obj,
						'message': chat_message
					}
				], countdown=delay)

				return task

			current_momoment = datetime.now().strftime('%d-%m-%Y %H:%M')
			response['timestamp'] = current_momoment

			await self.save_chat_message_obj(
				thread=thread_obj,
				user=user_obj,
				message=chat_message,
			)

			final_data_for_sending = {
				'type': 'chat_message',
				'text': json.dumps(response, cls=DjangoJSONEncoder)
			}

			await self.channel_layer.group_send(
				self.chat_room,
				final_data_for_sending
			)

	async def websocket_disconnect(self, event):
		print("disconnect", event)

	async def chat_message(self, event):
		await self.send({
			'type': 'websocket.send',
			'text':event['text']
		})

	@database_sync_to_async
	def get_thread(self, obj_id) -> Thread:
		return Thread.objects.get(id=obj_id)

	@database_sync_to_async
	def get_user(self, obj_id) -> User:
		return User.objects.get(id=obj_id)

	@database_sync_to_async
	def save_chat_message_obj(self,
						  	  thread: Thread=None,
		                  	  user: User=None,
		                  	  message: str=None) -> ChatMessage:

		if user:
			obj = ChatMessage.objects.create(
				thread_id=thread,
				user_id=user,
				message=message
			)
		else:
			obj = ChatMessage.objects.create(
				thread_id=thread,
				message=message
			)

		return obj

	async def get_seconds_until_future_datetime_point(self, delay_date,
		                                              delay_time):
		d, m, y = map(int, delay_date.split('/'))
		hours, minutes = map(int, delay_time.split(':'))

		future_time_point = datetime(y, m, d, hours, minutes)
		d_t_obj = datetime.now()
		current_time_point = datetime(d_t_obj.year,
									  d_t_obj.month,
			                          d_t_obj.day,
			                          d_t_obj.hour,
			                          d_t_obj.minute)
		difference = future_time_point - current_time_point
		seconds_to_wait = difference.total_seconds()
		return int(seconds_to_wait), future_time_point.strftime("%d-%m-%Y %H:%M")
