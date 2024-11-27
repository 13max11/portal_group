from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy

class RegistationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'auth_sys/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)