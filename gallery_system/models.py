from django.db import models

# Create your models here.

class GalleryItem(models.Model):
    title = models.CharField(max_length=32)
    img = models.ImageField(upload_to='images/gallery/')
    url = models.URLField(max_length=255, blank=True)

    class Meta:
        ordering = ['-id']