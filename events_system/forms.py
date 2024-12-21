from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    date_start = forms.DateTimeField (
        widget=forms.DateInput(attrs={'type': 'datetime-local'}),
        label="Дата початку"
    )
    date_end = forms.DateTimeField (
        widget=forms.DateInput(attrs={'type': 'datetime-local'}),
        label="Дата закінчення"
    )
    
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'date_start', 'date_end', 'img']
        labels = {
            'title': 'Заголовок',
            'description': 'Опис',
            'img': 'Зображення'
        }