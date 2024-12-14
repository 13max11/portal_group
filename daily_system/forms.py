from django import forms


class LessonFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', ''),
        ('present', 'Present'),
        ('missing', 'Missing'),]
    
   
    status = forms.ChoiceField(choices = STATUS_CHOICES, required=False, label='status')

class HomeworkFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('todo', 'To do'),
        ('in_progress', 'In progress'),
        ('done', 'Done'),]
   
    status = forms.ChoiceField(choices = STATUS_CHOICES, required=False, label='status')