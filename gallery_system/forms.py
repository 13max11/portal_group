from django import forms
from .models import GalleryItem

class GalleryItemForm(forms.ModelForm):
    title = forms.CharField(label="Заголовок", max_length=32)
    img = forms.ImageField(label="Фото")
    url = forms.URLField(label="URL-адреса", max_length=255, required=False)
    
    class Meta:
        model = GalleryItem
        fields = ['title', 'img', 'url']