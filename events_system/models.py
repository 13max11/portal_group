from django.db import models

# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=100,null=False)
    description = models.TextField()
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    img = models.FileField(upload_to="comments_media/", blank=True, null=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=100,null=False)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    img = models.FileField(upload_to="comments_media/", blank=True, null=True)

    def __str__(self):
        return self.title