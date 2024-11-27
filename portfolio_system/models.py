from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100,null=False)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="comments_media/", blank=True, null=True)
    img = models.FileField(upload_to="comments_media/", blank=True, null=True)
    video = models.FileField(upload_to="comments_media/", blank=True, null=True)

    def __str__(self):
        return self.title