from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages