from django import forms
from .models import Category, Topic, Comment, Poll, PollOption

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'only_mods']

class TopicForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        required=True
    )
    img = forms.ImageField(label="Завантажте сюди своє фото по бажанню", required=False)

    class Meta:
        model = Topic
        fields = ['category', 'title', 'content', 'img']

    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({
            'class': 'topics-select',
        })
        self.fields['title'].widget.attrs.update({
            'class': 'topics-input',
            'maxlength': '72',
            'placeholder': 'Введіть тему',
        })
        self.fields['content'].widget.attrs.update({
            'class': 'topics-textarea',
            'maxlength': '2500',
            'placeholder': 'Напишіть обсяг...',
        })

class TopicCategoryForm(forms.ModelForm):
    img = forms.ImageField(label="Завантажте сюди своє фото по бажанню", required=False)

    class Meta:
        model = Topic
        fields = ['title', 'content', 'img']

    def __init__(self, *args, **kwargs):
        super(TopicCategoryForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'topics-input',
            'maxlength': '72',
            'placeholder': 'Введіть тему',
        })
        self.fields['content'].widget.attrs.update({
            'class': 'topics-textarea',
            'maxlength': '2500',
            'placeholder': 'Напишіть обсяг...',
        })

class TopicSortForm(forms.Form):
    SORT_BY_CHOICES = [
        ('-id', 'по даті створення'),
        ('title', 'по алфавіту'),
        ('likes', 'по рейтингу'),
        ('last', 'останні переглянуті'),
    ]

    sort_by = forms.ChoiceField(choices=SORT_BY_CHOICES, required=False, label='сортувати по:')

class CategorySortForm(forms.Form):
    SORT_BY_CHOICES = [
        ('name', 'по алфавіту'),
        ('-id', 'по даті створення'),
        ('topics', 'по кількості топіків'),
        ('last', 'останні переглянуті'),
    ]

    sort_by = forms.ChoiceField(choices=SORT_BY_CHOICES, required=False, label='сортувати по:')


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