from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Topic, Comment, Like
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from .forms import TopicForm, CategoryForm, Category


'''@login_required
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
    return render(request, 'forum_system/create_topic.html', {'category': category})'''

'''def topic_detail(request, pk):
    topic = get_object_or_404(Topic, id=pk)
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
    })'''


class TopicCreateView(LoginRequiredMixin, CreateView):
    template_name = 'forum_system/create_topic.html'
    form_class = TopicForm
    success_url = reverse_lazy('category')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TopicDetailView(DetailView):
    model = Topic
    template_name = 'forum_system/topic_detail.html'
    context_object_name = 'topic'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['likes_count'] = self.object.likes.count()
        return context
    
    def post(self, request, *args, **kwargs):
        topic = self.get_object()

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
                    existing_like.delete()  # Удалить лайк, якщо вже існує
                else:
                    Like.objects.create(topic=topic, user=request.user)
            else:
                return HttpResponseForbidden("You must be logged in to like a topic.")
        
        # Redirect to the same page after processing the POST request
        return redirect('topic-detail', pk=topic.pk)

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'forum_system/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = self.object.topics.all()
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'forum_system/categorys.html'
    context_object_name = 'categorys'

def index(request):
    categories = Category.objects.all()
    form = None

    # Только администратор может видеть и использовать форму
    if request.user.is_staff:
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = CategoryForm()

    return render(request, 'forum_system/index.html', {
        'categories': categories,
        'form': form
    })