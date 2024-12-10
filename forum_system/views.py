from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Topic, Comment, Like
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from .forms import TopicForm, CategoryForm, Category, PollForm, PollOptionFormSet, TopicForm
from .models import Poll, PollOption, Topic, Vote


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
    success_url = reverse_lazy('forum')

    def form_valid(self, form):
        # Создаем Topic
        form.instance.created_by = self.request.user
        topic = form.save()

        # Проверяем и обрабатываем голосования
        polls_count = int(self.request.POST.get('polls_count', 0))  # Сколько голосований создал пользователь
        for i in range(polls_count):
            poll_title = self.request.POST.get(f'polls[{i}][title]')
            poll_question = self.request.POST.get(f'polls[{i}][question]')
            if poll_title and poll_question:
                # Создаем голосование
                poll = Poll.objects.create(topic=topic, title=poll_title, question=poll_question)

                # Добавляем варианты ответа
                option_idx = 0
                while True:
                    option_text = self.request.POST.get(f'polls[{i}][options][{option_idx}]')
                    if option_text:
                        option = PollOption.objects.create(poll=poll, text=option_text)
                        option_idx += 1
                    else:
                        break  # Завершаем, когда опции заканчиваются
                        
        return redirect(self.success_url)


class TopicDetailView(DetailView):
    model = Topic
    template_name = 'forum_system/topic_detail.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем все голосования для текущего топика
        polls = self.object.polls.prefetch_related('options')
        context['polls'] = polls

        # Проверяем, голосовал ли пользователь
        user_vote_texts = {}
        if self.request.user.is_authenticated:
            for poll in polls:
                user_vote = poll.options.filter(votes=self.request.user).first()
                if user_vote:
                    user_vote_texts[poll.pk] = user_vote.text
        context['user_vote_texts'] = user_vote_texts

        # Дополнительный контекст
        context['comments'] = self.object.comments.all()
        context['likes_count'] = self.object.likes.count()
        return context

    def post(self, request, *args, **kwargs):
        topic = self.get_object()

        # Обработка голосования

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

        if "vote" in request.POST:
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must log in to vote.")

            poll_id = request.POST.get('poll_id')
            option_id = request.POST.get('vote')
            try:
                option = PollOption.objects.get(pk=option_id)
                if not option.votes.filter(id=request.user.id).exists():
                    option.votes.add(request.user)
            except PollOption.DoesNotExist:
                pass
            return redirect('topic-detail', pk=topic.pk)

        # Обработка лайков
        if "like" in request.POST:
            if request.user.is_authenticated:
                existing_like = Like.objects.filter(topic=topic, user=request.user).first()
                if existing_like:
                    existing_like.delete()
                else:
                    Like.objects.create(topic=topic, user=request.user)
            else:
                return HttpResponseForbidden("You must log in to like.")

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

    return render(request, 'forum_system/index.html')

def forum(request):
    categories = Category.objects.all()
    form = None

    if request.user.is_staff:
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('forum')
        else:
            form = CategoryForm()

    return render(request, 'forum_system/forum.html', {
        'categories': categories,
        'form': form
    })

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

def create_poll(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        formset = PollOptionFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            poll = form.save()
            options = formset.save(commit=False)
            for option in options:
                option.poll = poll
                option.save()
            return redirect('index')  # Перенаправление на главную страницу
    else:
        form = PollForm()
        formset = PollOptionFormSet()

    return render(request, 'forum_system/create_poll.html', {'form': form, 'formset': formset})