from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")


from django import forms
from django.contrib.auth.models import User

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'description', 'avatar']

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)

class ChangeAvatarForm(forms.Form):
    avatar = forms.ImageField()

class ChangeEmailForm(forms.Form):
    email = forms.EmailField()

class ChangePhoneNumberForm(forms.Form):
    phone_number = forms.CharField()

class ChangeDescriptionForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea)