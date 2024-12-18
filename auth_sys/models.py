from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=64, blank=False, null=False)
    last_name = models.CharField(max_length=64, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    email_show = models.BooleanField(blank=True, null=True)

    avatar = models.ImageField(upload_to='images/avatars/', default='images/avatars/default.jpg')
    description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    phone_number_show = models.BooleanField(blank=True, null=True)

    def __str__(self) -> str:
        return self.username
    

class Project(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    media = models.FileField(upload_to='media/images/portfolio/', null=True, blank=True)

    def __str__(self) -> str:
        return self.title


