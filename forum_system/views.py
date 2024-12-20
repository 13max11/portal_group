from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Topic, Comment, Like
from events_system.models import Event
from auth_sys.models import TopicView, CategoryView

from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy

from .forms import TopicForm, TopicCategoryForm, TopicSortForm, CategoryForm, CategorySortForm, Category, PollForm, PollOptionForm
from django.http import JsonResponse
from .models import Topic, Poll, PollOption, PollVote

from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q, F


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


@login_required
def topic_create_view(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            if topic.category.only_mods and not request.user.is_staff:
                messages.error(request, "Тільки модератори можуть створювати теми в цій категорії.")
                return redirect('forum')
            topic.created_by = request.user
            topic.save()
            return redirect('topic-detail', pk=topic.pk)
    else:
        form = TopicForm()

    return render(request, 'forum_system/create_topic.html', {'form': form})

@login_required
def topic_create_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if category.only_mods and not request.user.is_staff:
        return redirect('category-detail', category.pk)

    if request.method == 'POST':
        form = TopicCategoryForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            form.instance.category = category
            form.save()
            return redirect('topic-detail', pk=form.instance.pk)
    else:
        form = TopicCategoryForm()

    return render(request, 'forum_system/create_topic_category.html', {
        'category': category, 
        'form': form
    })


class TopicDetailView(DetailView):
    model = Topic
    template_name = 'forum_system/topic_detail.html'
    context_object_name = 'topic'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['likes_count'] = self.object.likes.count()
        return context
    
    def get_object(self, queryset=None):
        # Отримуємо об'єкт теми
        topic = super().get_object(queryset)

        # Перевіряємо, чи користувач автентифікований
        if self.request.user.is_authenticated:
            # Зберігаємо перегляд теми
            TopicView.objects.update_or_create(
                user=self.request.user,
                topic=topic,
                defaults={'viewed_at': timezone.now()}
            )
        return topic
    
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
        context['form'] = TopicSortForm()

        sort_by = self.request.GET.get('sort_by', '-id')
        context['form'] = TopicSortForm(initial={'sort_by': sort_by})

        if sort_by == 'title':
            context['topics'] = self.object.topics.all().order_by('title')
        elif sort_by == '-id':
            context['topics'] = self.object.topics.all().order_by('-id')
        elif sort_by == 'likes':
            context['topics'] = self.object.topics.all().annotate(likes_count=Count('likes')).order_by('-likes_count')
        elif sort_by == 'last':
            context['topics'] = self.object.topics.filter(
                topicview__user=self.request.user
            ).annotate(
                viewed_at=F('topicview__viewed_at')
            ).order_by('-viewed_at')
        else:
            context['topics'] = self.object.topics.all().order_by('-id')

        return context

    def get_object(self, queryset=None):
        category = super().get_object(queryset)

        if self.request.user.is_authenticated:
            CategoryView.objects.update_or_create(
                user=self.request.user,
                category=category,
                defaults={'viewed_at': timezone.now()}
            )
        return category

class CategoryListView(ListView):
    model = Category
    template_name = 'forum_system/categorys.html'
    context_object_name = 'categorys'

def index(request):
    events = Event.objects.filter(date_end__gte=timezone.now()).order_by('date_end','date_start')[:3]
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
    topics = Topic.objects.all().order_by('-created_at')[:3]

    sort_form = CategorySortForm()

    sort_by = request.GET.get('sort_by', 'name')

    sort_form = CategorySortForm(initial={'sort_by': sort_by})
    
    if sort_by == 'title':
        categories = Category.objects.all().order_by('name')
    elif sort_by == '-id':
        categories = Category.objects.all().order_by('-id')
    elif sort_by == 'topics':
        categories = Category.objects.all().annotate(topics_count=Count('topics')).order_by('-topics_count')
    elif sort_by == 'last':
        categories = Category.objects.filter(
            categoryview__user=request.user
        ).annotate(
            viewed_at=F('categoryview__viewed_at')
        ).order_by('-viewed_at')
    else:
        categories = Category.objects.all().order_by('name')

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
        'sort_form': sort_form,
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
        form.instance.updated = True
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
        return redirect('login') # Перенаправлення на головну сторінку форуму
    
    # Отримуємо топік за його ID
    topic = get_object_or_404(Topic, pk=pk)
    topic_category = topic.category.pk

    # Перевіряємо, чи користувач є автором теми
    if topic.created_by != request.user and not request.user.is_staff:
        messages.error(request, "You cannot delet this topic.")
        return redirect('topic-detail', topic.pk)
    
    # Видаляємо топик
    topic.delete()
    messages.success(request, "Topic deleted successfully")
    return redirect('category-detail', topic_category)