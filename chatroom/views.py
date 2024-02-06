from rest_framework import generics
from .models import Message
from .api.serializer import MessageSerializer




class ListMessages(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    ordering = ('-timestamp')
