from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Topic, Comment, Like
from events_system.models import Event
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy

from .forms import TopicForm, CategoryForm, Category, PollForm, PollOptionForm
from django.http import JsonResponse
from .models import Topic, Poll, PollOption, PollVote

from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q


@login_required
def create_poll(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        if poll_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.topic = topic
            poll.save()
            return redirect('topic-detail', pk=topic_id)
    else:
        poll_form = PollForm()

    return render(request, 'forum_system/create_poll.html', {'form': poll_form, 'topic': topic})

@login_required
def add_poll_option(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.method == 'POST':
        option_form = PollOptionForm(request.POST)
        if option_form.is_valid():
            option = option_form.save(commit=False)
            option.poll = poll
            option.save()
            return redirect('topic-detail', pk=poll.topic.id)
    else:
        option_form = PollOptionForm()

    return render(request, 'forum_system/add_poll_option.html', {'form': option_form, 'poll': poll})

@login_required
def vote_poll(request, pk):
    option = get_object_or_404(PollOption, id=pk)
    poll = option.poll

    if not PollVote.objects.filter(option__poll=poll, user=request.user).exists():
        PollVote.objects.create(option=option, user=request.user)
        option.votes += 1
        option.save()

    return JsonResponse({
        'success': True,
        'poll_results': [
            {
                'text': o.text,
                'votes': o.votes,
                'percentage': o.votes * 100 / sum(opt.votes for opt in poll.options.all())
            } for o in poll.options.all()
        ]
    })

@login_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if poll.topic.created_by == request.user:
        poll.delete()
    return redirect('topic-detail', pk=poll.topic.id)

@login_required
def delete_poll_option(request, option_id):
    option = get_object_or_404(PollOption, id=option_id)
    poll = option.poll
    if poll.topic.created_by == request.user:
        option.delete()
    return redirect('topic-detail', pk=poll.topic.id)


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
        self.object = form.save()
        return redirect('topic-detail', pk=self.object.pk)  # Перенаправляем на страницу с деталями топика


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

        # Обработка лайков
        if "like" in request.POST:
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
    events = Event.objects.filter(date_start__gte=timezone.now()).order_by('date_start')[:3]
    one_week_ago = timezone.now() - timedelta(days=7)
    
    categories = Category.objects.annotate(
        topic_count=Count('topics', filter=Q(topics__created_at__gte=one_week_ago))
    ).order_by('-topic_count')[:5]
    form = None

    context = {
        'categories': categories,
        'events': events,
    }

    return render(request, 'forum_system/index.html', context)

def forum(request):
    categories = Category.objects.all()
    topics = Topic.objects.all().order_by('?')[:3]
    form = None

    if request.user.is_staff:
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('forum')
        else:
            form = CategoryForm()

    context = {
        'categories': categories,
        'topics': topics,
        'form': form,
    }

    return render(request, 'forum_system/forum.html', context)

def create_category(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = CategoryForm()
    
    else:
        return redirect('forum')
    
    return render(request, 'forum_system/create_category.html', {'form':form})

def update_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    # Проверяем, что текущий пользователь является автором поста
    if topic.created_by != request.user:
        return redirect('topic-detail', pk=pk)

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('topic-detail', pk=pk)
    else:
        form = TopicForm(instance=topic)

    return render(request, 'forum_system/update_topic.html', {'form': form, 'topic': topic})

def delete_topic(request, pk):
    # Перевіряємо, чи користувач авторизований
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to delete a topic.")
        return redirect('forum_home') # Перенаправлення на головну сторінку форуму
    
    # Отримуємо топік за його ID
    topic = get_object_or_404(Topic, pk=pk)
    topic_category = topic.category.pk

    # Перевіряємо, чи користувач є автором теми
    if topic.created_by != request.user:
        messages.error(request, "You cannot delet this topic.")
        return redirect('topic-detail', topic.pk)
    
    # Видаляємо топик
    topic.delete()
    messages.success(request, "Topic deleted successfully")
    return redirect('category-detail', topic_category)