from statistics import mode
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from rest_framework.authtoken.models import Token
from django_userforeignkey.models.fields import UserForeignKey

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class OTP(models.Model):
    user = models.CharField(max_length=10,default=1)
    otp = models.CharField(max_length=6)


    def __str__(self): 
        return self.user 