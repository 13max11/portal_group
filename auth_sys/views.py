from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, TemplateView
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse_lazy

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

