from django.conf import settings

from rest_framework import serializers

from .models import ChatMessage


class ChatMessagesSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%d-%m-%Y %H:%M',
                                          required=False, read_only=True)

    username = serializers.ReadOnlyField(source='user_id.username')

    class Meta:
        model = ChatMessage
        fields = '__all__'