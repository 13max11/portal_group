from django import forms
from .models import Category, Topic, Comment, Poll, PollOption
from django.forms import modelformset_factory

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class TopicForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)

    class Meta:
        model = Topic
        fields = ['category', 'title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'question']


class PollOptionForm(forms.ModelForm):
    class Meta:
        model = PollOption
        fields = ['text']

# Создаём модульный формсет для добавления нескольких вариантов голосования
PollOptionFormSet = modelformset_factory(
    PollOption, 
    form=PollOptionForm, 
    extra=3,  # 3 пустых варианта по умолчанию
    can_delete=True
)