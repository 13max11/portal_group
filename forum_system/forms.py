from django import forms
from .models import Category, Topic, Comment, Poll, PollOption

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
        fields = ['name', 'description']

class PollOptionForm(forms.ModelForm):
    class Meta:
        model = PollOption
        fields = ['text']