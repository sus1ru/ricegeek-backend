from django.db import models
from django_userforeignkey.models.fields import UserForeignKey
from cloudinary.models import CloudinaryField

# Create your models here.

class UserProfileModel(models.Model):
    user = UserForeignKey(auto_user_add=True)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=150)
    profileimage = CloudinaryField('profileimage')

    def __str__(self): 
        return self.username