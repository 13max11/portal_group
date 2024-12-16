from django import forms
from .models import Lesson

class LessonFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('missing', 'Missing'),]
    
   
    status = forms.ChoiceField(choices = STATUS_CHOICES, required=False, label='status')

class HomeworkFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('done', "Done"),
        ('in_progress', "In progress"),
        ('to_do', "To do"),] 
   
    status = forms.ChoiceField(choices = STATUS_CHOICES, required=False, label='status') 
