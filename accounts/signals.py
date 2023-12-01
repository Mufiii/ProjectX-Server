from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from vendor.models import BusinessVendor
from developer.models import Developer



@receiver(post_save, sender=User)
def create_UserProfile(sender, instance, created, **kwargs):
    if created:
        if instance.is_developer:
            Developer.objects.create(user=instance)
        elif instance.is_vendor:
            BusinessVendor.objects.create(user=instance)
            


