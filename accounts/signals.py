from django.db.models.signals import post_save
from django.dispatch import receiver
from developer.models import Developer
from vendor.models import BusinessVendor
from .models import User
from monitorization.models import Workspace


@receiver(post_save, sender=User)
def create_UserProfile(sender, instance, created, **kwargs):
    if created:
        if instance.is_developer:
            Developer.objects.create(user=instance)
        elif instance.is_vendor:
            BusinessVendor.objects.create(user=instance)


@receiver(post_save,sender=User)
def Create_Workspace(sender,instance,created, **kwargs):
    if created :
        first_name = instance.first_name
        last_name = instance.last_name
        
        Workspace.objects.create(
            user=instance, 
            name=f"{first_name} {last_name}'s Workspace"
        )
        instance.save()