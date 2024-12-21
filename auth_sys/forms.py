from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Project
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'description']

class AvatarForm(forms.Form):
    avatar = forms.ImageField()

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'media']
        
    def clean_media(self):
        media = self.cleaned_data.get('media')
        if media:
            # Перевіряємо розмір файлу (наприклад, максимум 5MB)
            if media.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Файл занадто великий. Максимальний розмір - 5MB')
            
            # Перевіряємо тип файлу
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'video/mp4']
            if media.content_type not in allowed_types:
                raise forms.ValidationError('Непідтримуваний тип файлу')
                
        return media
