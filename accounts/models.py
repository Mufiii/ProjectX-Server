from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from django.utils import timezone

class User(AbstractUser):
    # three user admin developer vendor
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True, unique=False)
    phone = models.CharField(max_length=13, null=True, blank=True)
    country = CountryField(blank_label="(select country)", null=True, blank=True)
    otp = models.CharField(
        max_length=8, verbose_name="one-time-password", blank=True, null=True
    )
    otp_expiry = models.DateTimeField(null=True, blank=True)
    is_developer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
    
    def is_otp_expired(self):
        if self.otp_expiry is None:
            return True
        return self.otp_expiry < timezone.now()
