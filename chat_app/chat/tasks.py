from celery import shared_task
from celery.decorators import task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

from .models import ChatMessage


@shared_task(serializer='pickle')
def send_delayed_message(chat_room, data, data_for_creation):

    if not data_for_creation['message']:
        return

    ChatMessage.objects.create(
        thread_id=data_for_creation['thread_obj'],
        user_id=data_for_creation['user_obj'],
        message=data_for_creation['message']
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(chat_room, data)
