from django.urls import path

from . import consumers


app_name = 'chat'

url_patterns = [
   path('thread/<int:thread_id>/', consumers.ChatConsumer.as_asgi())
]
