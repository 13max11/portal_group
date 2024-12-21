from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, TemplateView
from .models import CustomUser, Project, TopicView, Topic
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, PortfolioForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied


def auth_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'auth_sys/auth_page.html')

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


def can_edit_profile(request_user, profile_user):
    # Користувач може редагувати свій профіль
    if request_user == profile_user:
        return True
        
    # Admin може редагувати всіх
    if request_user.is_superuser:
        return True
        
    # Moderator може редагувати звичайних користувачів
    if request_user.is_staff and not profile_user.is_staff and not profile_user.is_superuser:
        return True
        
    return False

@login_required
def profile_view(request, username):
    User = get_user_model()
    profile_user = get_object_or_404(User, username=username)
    
    # Перевіряємо права доступу
    can_edit = can_edit_profile(request.user, profile_user)
    
    # Отримуємо теми користувача
    user_topics = Topic.objects.filter(created_by=profile_user).order_by('-created_at')
    
    # Отримуємо проекти портфоліо користувача, чий профіль переглядається
    portfolio_items = Project.objects.filter(user=profile_user)
    
    context = {
        'profile_user': profile_user,
        'user_topics': user_topics,
        'portfolio_items': portfolio_items,
        'can_edit': can_edit,
    }
    
    return render(request, 'auth_sys/profile.html', context)

@login_required
def profile_update(request):
    if request.method == 'POST':
        user = request.user
        target_user = get_object_or_404(get_user_model(), username=request.POST.get('username', user.username))
        
        if not can_edit_profile(request.user, target_user):
            raise PermissionDenied("У вас немає прав для редагування цього профілю")
            
        try:
            if 'avatar' in request.FILES:
                if target_user.avatar:
                    target_user.avatar.delete(save=False)
                target_user.avatar = request.FILES['avatar']
            
            if 'first_name' in request.POST:
                target_user.first_name = request.POST['first_name']
            if 'last_name' in request.POST:
                target_user.last_name = request.POST['last_name']
            if 'email' in request.POST:
                target_user.email = request.POST['email']
            if 'phone_number' in request.POST:
                target_user.phone_number = request.POST['phone_number']
            if 'description' in request.POST:
                target_user.description = request.POST['description']

            target_user.save()
            messages.success(request, 'Профіль успішно оновлено!')
        except Exception as e:
            messages.error(request, f'Помилка при оновленні профілю: {str(e)}')
            
    return redirect('profile', username=target_user.username)


@login_required
def portfolio_view(request):
    # Отримуємо всі проекти для відображення в загальному списку
    portfolio_items = Project.objects.all().order_by('-id')
    return render(request, 'auth_sys/profile.html', {'portfolio_items': portfolio_items})

@login_required
def portfolio_add(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                project = form.save(commit=False)
                project.user = request.user  # Зберігаємо поточного користувача як власника
                project.save()
                return JsonResponse({'status': 'success'})
            else:
                print("Form errors:", form.errors)
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        except Exception as e:
            print("Exception:", str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        form = PortfolioForm()
    return render(request, 'auth_sys/profile.html', {'form': form})


def view_history(request):
    topics = TopicView.objects.filter(user=request.user)

    context = {
        'topics_history': topics,
    }

    return render(request, 'auth_sys/view_history.html', context)

@login_required
@require_http_methods(["DELETE"])
def portfolio_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Перевіряємо права доступу
    if not can_edit_profile(request.user, project.user):
        return JsonResponse({
            'status': 'error',
            'message': 'У вас немає прав для видалення цього проекту'
        }, status=403)
    
    try:
        project.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required
def portfolio_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Перевіряємо права доступу
    if not can_edit_profile(request.user, project.user):
        return JsonResponse({
            'status': 'error',
            'message': 'У вас немає прав для редагування цього проекту'
        }, status=403)
    
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    data = {
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'media_url': project.media.url if project.media else None
    }
    return JsonResponse(data)