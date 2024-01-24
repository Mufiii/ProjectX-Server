from django.contrib import admin
from .models import Message,MessageMedia
# Register your models here.


admin.site.register(MessageMedia)
admin.site.register(Message)
