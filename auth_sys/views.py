from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, TemplateView
from .models import CustomUser, Project, TopicView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, PortfolioForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth import get_user_model


class AuthPageView(TemplateView):
    template_name = 'auth_sys/auth_page.html'

def registration(request):
    if request.user.is_authenticated:
        return redirect('index')

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
def profile_view(request, username):
    User = get_user_model()
    profile_user = get_object_or_404(User, username=username)
    return render(request, 'auth_sys/profile.html', {'profile_user': profile_user})

@login_required
def profile_update(request):
    if request.method == 'POST':
        user = request.user
        
        if 'first_name' in request.POST:
            user.first_name = request.POST['first_name']
        if 'last_name' in request.POST:
            user.last_name = request.POST['last_name']
        if 'email' in request.POST:
            user.email = request.POST['email']
        if 'phone_number' in request.POST:
            user.phone_number = request.POST['phone_number']
        if 'description' in request.POST:
            user.description = request.POST['description']
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        user.save()
        messages.success(request, 'Профіль успішно оновлено!')
        
    return redirect('profile', username=request.user.username)


@login_required
def portfolio_view(request):
    portfolio_items = Project.objects.filter(user=request.user)
    return render(request, 'auth_sys/portfolio.html', {'portfolio_items': portfolio_items})

@login_required
def portfolio_add(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('portfolio')
    else:
        form = PortfolioForm()
    return render(request, 'auth_sys/portfolio.html', {'form': form})


def view_history(request):
    topics = TopicView.objects.filter(user=request.user)

    context = {
        'topics_history': topics,
    }

    return render(request, 'auth_sys/view_history.html', context)