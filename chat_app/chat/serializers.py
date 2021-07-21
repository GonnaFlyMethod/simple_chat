from .models import ChatMessage

from rest_framework import  serializers


class ChatMessagesSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%d-%m-%Y %H:%M',
                                          required=False, read_only=True)

    class Meta:
        model = ChatMessage
        fields = '__all__'