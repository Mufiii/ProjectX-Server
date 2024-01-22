from django.db.models.signals import post_save
from django.dispatch import receiver 
from monitorization.models import Workspace
from django.utils.text import slugify
import random
import string



@receiver(post_save, sender=Workspace)
def create_short_name_for_workspace(sender, instance, created, **kwargs):
    if created:
        random_number = ''.join(random.choices(string.digits, k=8))
        short_name = slugify(instance.name.lower()) + random_number
        instance.short_name = short_name
        instance.save(update_fields=['short_name'])  # Prevent infinite loop
