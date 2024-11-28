from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Topic, Comment, Like
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden


@login_required
def create_topic(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title and content:
            Topic.objects.create(
                category=category,
                title=title,
                content=content,
                created_by=request.user
            )
            return redirect('category-detail', category_id=category.id)
        else:
            messages.error(request, "Title and content are required.")
    return render(request, 'forum_system/create_topic.html', {'category': category})


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == "POST":
        if "comment" in request.POST:
            content = request.POST.get("content")
            if content:
                Comment.objects.create(
                    topic=topic,
                    content=content,
                    created_by=request.user
                )
            else:
                messages.error(request, "Comment cannot be empty.")
        elif "like" in request.POST:
            if request.user.is_authenticated:
                existing_like = Like.objects.filter(topic=topic, user=request.user).first()
                if existing_like:
                    existing_like.delete()  # Удалить лайк, если уже существует
                else:
                    Like.objects.create(topic=topic, user=request.user)
            else:
                return HttpResponseForbidden("You must be logged in to like a topic.")

    comments = topic.comments.all()
    likes_count = topic.likes.count()
    return render(request, 'forum_system/topic_detail.html', {
        'topic': topic,
        'comments': comments,
        'likes_count': likes_count
    })

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    topics = category.topics.all()
    return render(request, 'forum_system/category_detail.html', {
        'category': category,
        'topics': topics
    })

def index(request):
    categories = Category.objects.all()  # Получаем все категории
    return render(request, 'forum_system/index.html', {'categories': categories})