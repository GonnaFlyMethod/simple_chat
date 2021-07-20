import asyncio
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage


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

			response = {
				'message': chat_message,
			}

			if is_anonymous_message:
				response['current_user_username'] = 'Anonymous'
				user_obj: User = await self.get_user(current_user_id)
			else:
				response['current_user_username'] = current_user_username
				user_obj = None

			thread_obj: Thread = await self.get_thread(current_thread_id)
			
			chat_message_obj = await self.save_chat_message(
				thread=thread_obj,
				user=user_obj,
				message=chat_message,
			)

			response['timestamp'] = chat_message_obj.timestamp

			await self.channel_layer.group_send(
				self.chat_room,
				{
					'type': 'chat_message',
					'text': json.dumps(response, cls=DjangoJSONEncoder)
				}
			)

	async def websocket_disconnect(self, event):
		print("disconnect", event)

	async def chat_message(self, event):
		print("sended")
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
	def save_chat_message(self,
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
