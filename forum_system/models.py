from django.db import models
from django.conf import settings  # Для использования AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Используем AUTH_USER_MODEL
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Используем AUTH_USER_MODEL
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.created_by} on {self.topic}"

class Like(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Используем AUTH_USER_MODEL
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("topic", "user")

# Модели для системы голосований
class Poll(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, related_name="polls")
    question = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_votes(self):
        """Подсчет общего количества голосов"""
        return sum(option.votes.count() for option in self.options.all())


class PollOption(models.Model):
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    votes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="poll_votes",
        blank=True
    )

    def percentage(self):
        """Возвращает процент голосов"""
        total_votes = self.poll.total_votes()
        return (self.votes.count() / total_votes * 100) if total_votes > 0 else 0



class Vote(models.Model):
    option = models.ForeignKey(
        PollOption, 
        on_delete=models.CASCADE, 
        related_name="votes_cast"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('option', 'user')  # Пользователь может голосовать за один вариант только один раз