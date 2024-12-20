from django.db import models
from django.contrib.auth.models import AbstractUser
from forum_system.models import Topic, Category

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

class TopicView(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        unique_together = ('user', 'topic')

    def __str__(self):
        return f"{self.user.username} viewed {self.topic.title} at {self.viewed_at}"

class CategoryView(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.user.username} viewed {self.category.name} at {self.viewed_at}"
    

class Project(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    media = models.FileField(upload_to='media/images/portfolio/', null=True, blank=True)

    def __str__(self) -> str:
        return self.title


