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
