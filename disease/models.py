from email.mime import image
from django.db import models

# Create your models here.

class Disease(models.Model):
    name = models.CharField(max_length=30)
    image = models.CharField(max_length=300,null=True)
    symptoms = models.CharField(max_length=300,null=True)
    recommendations = models.CharField(max_length=300,null=True)
    organiccontrol = models.CharField(max_length=150,null=True)
    chemicalcontrol = models.CharField(max_length=150,null=True)

    def __str__(self):
        return self.name