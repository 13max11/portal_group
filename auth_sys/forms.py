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
        fields = ['title', 'description', 'media', 'link', 'link_title']
        
    def clean_media(self):
        media = self.cleaned_data.get('media')
        if media:
            # Отримуємо розширення файлу
            file_extension = media.name.split('.')[-1].lower()
            
            # Дозволені розширення
            allowed_image_types = ['jpg', 'jpeg', 'png', 'gif']
            allowed_video_types = ['mp4', 'webm', 'mov']
            
            if file_extension not in allowed_image_types + allowed_video_types:
                raise forms.ValidationError('Непідтримуваний тип файлу. Дозволені формати: jpg, jpeg, png, gif, mp4, webm, mov')
            
            # Збільшуємо максимальний розмір до 50MB для відео
            if media.size > 50 * 1024 * 1024:  # 50MB
                raise forms.ValidationError('Файл занадто великий. Максимальний розмір - 50MB')
                
        return media
