from django.db import models
from accounts.models import User
import uuid





class MessageMedia(models.Model):
    media = models.FileField(upload_to='media/', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    media = models.ForeignKey(MessageMedia, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    message_type = models.CharField(
        choices=[('text', 'Text'), 
                 ('audio', 'Audio'), 
                 ('video', 'Video')], 
                  max_length=10,
                  blank=True , null=True
    )
    seen = models.BooleanField(default=False)
    
    class Meta:
        db_table = "chat_message"
        ordering = ("timestamp",)
    
    
    def __str__(self):
        return self.sender