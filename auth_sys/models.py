from django.db import models
from django.contrib.auth.models import AbstractUser
from forum_system.models import Topic, Category
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import sys

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

    def save(self, *args, **kwargs):
        # Якщо є нова аватарка
        if self.avatar:
            # Відкриваємо зображення
            img = Image.open(self.avatar)
            
            # Конвертуємо в RGB якщо потрібно
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Зберігаємо в буфер
            output = BytesIO()
            img.save(output, format='JPEG', quality=90)
            output.seek(0)
            
            # Замінюємо оригінальний файл на оброблений
            self.avatar = InMemoryUploadedFile(
                output,
                'ImageField',
                f"{self.avatar.name.split('.')[0]}.jpg",
                'image/jpeg',
                sys.getsizeof(output),
                None
            )
            
        super().save(*args, **kwargs)

class TopicView(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topic = models.ForeignKey('forum_system.Topic', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        unique_together = ('user', 'topic')

    def __str__(self):
        return f"{self.user.username} viewed {self.topic.title} at {self.viewed_at}"

class CategoryView(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey('forum_system.Category', on_delete=models.CASCADE)
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
    link = models.URLField(max_length=200, null=True, blank=True)
    link_title = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return self.title

class QuickAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quick_accounts')
    quick_access_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quick_accessed_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'quick_access_to')

class SavedAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved_accounts')
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)  # Зберігаємо незашифрований пароль
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'username')


