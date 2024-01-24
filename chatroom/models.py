from django.db import models
from accounts.models import User





class MessageMedia(models.Model):
    media = models.FileField(upload_to='media/', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    media = models.ForeignKey(MessageMedia, on_delete=models.CASCADE, null=True, blank=True)
    message_type = models.CharField(
        choices=[('text', 'Text'), 
                 ('audio', 'Audio'), 
                 ('video', 'Video')], 
                  max_length=10
    )
    seen = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.sender