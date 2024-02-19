from django.db import models
import uuid
from accounts.models import User



class ChatRoom(models.Model):
		roomId = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
		room_type = models.CharField(max_length=10, default='DM')
		member = models.ManyToManyField(User)
		name = models.CharField(max_length=20, null=True, blank=True)

		def __str__(self):
			return self.room_id + ' -> ' + str(self.name)

class ChatMessage(models.Model):
		chat = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True)
		user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
		message = models.CharField(max_length=255)
		timestamp = models.DateTimeField(auto_now_add=True)

		def __str__(self):
			return self.message


class OnlineUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username


# class MessageMedia(models.Model):
#     media = models.FileField(upload_to='media/', null=False, blank=False)
#     created_at = models.DateTimeField(auto_now_add=True)


# class Room(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100)
    
#     def __str__(self) -> str:
#         return self.name


# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     media = models.ForeignKey(MessageMedia, on_delete=models.CASCADE, null=True, blank=True)
#     room = models.ForeignKey(Room,on_delete=models.CASCADE)
#     message_type = models.CharField(
#         choices=[('text', 'Text'), 
#                  ('audio', 'Audio'), 
#                  ('video', 'Video')], 
#                   max_length=10,
#                   blank=True , null=True
#     )
#     seen = models.BooleanField(default=False)
    
#     class Meta:
#         db_table = "chat_message"
#         ordering = ("timestamp",)
    
    
#     def __str__(self):
#         return self.sender