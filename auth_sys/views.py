from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, TemplateView
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ProfileUpdateForm, ChangePasswordForm, ChangeAvatarForm, ChangeEmailForm, ChangePhoneNumberForm, ChangeDescriptionForm


class AuthPageView(TemplateView):
    template_name = 'auth_sys/auth_page.html'

def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth_sys/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def profile_view(request):
    user = request.user
    viewer = request.user  # Це поточний залогінений користувач
    return render(request, 'profile.html', {'user': user, 'viewer': viewer})

@login_required
def profile_update(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile-view')  # Після збереження редіректимо на профіль
    else:
        form = ProfileUpdateForm(instance=user)
    return render(request, 'profile_update.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Оновлюємо сесію після зміни пароля
            return redirect('profile-view')  # Перенаправляємо на профіль після зміни пароля
    else:
        form = ChangePasswordForm(request.user)

@login_required
def change_avatar(request):
    if request.method == 'POST' and request.FILES['avatar']:
        avatar = request.FILES['avatar']
        fs = FileSystemStorage()
        filename = fs.save(avatar.name, avatar)
        user = request.user
        user.avatar = filename  # Оновлюємо аватар
        user.save()
        return redirect('profile-view')
    return render(request, 'change_avatar.html')

@login_required
def change_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = request.user
        user.email = email
        user.save()
        return redirect('profile-view')
    return render(request, 'change_email.html')

@login_required
def change_phone_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        user = request.user
        user.phone_number = phone_number
        user.save()
        return redirect('profile-view')
    return render(request, 'change_phone_number.html')

@login_required
def change_description(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        user = request.user
        user.description = description
        user.save()
        return redirect('profile-view')
    return render(request, 'change_description.html')