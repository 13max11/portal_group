from django import forms
from .models import Lesson

class LessonFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('present', 'Присутній'),
        ('missing', 'Відсутній'),]
    
   
    status = forms.ChoiceField(choices = STATUS_CHOICES, required=False, label='status')

class HomeworkFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('done', "Зроблено"),
        ('in_progress', "В процесі"),
        ('to_do', "Треба зробити"),] 
   
    status = forms.ChoiceField(choices = STATUS_CHOICES, required=False, label='status') 
