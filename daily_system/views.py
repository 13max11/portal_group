from django.shortcuts import render
from .models import Lesson, Homework
from django.views.generic import ListView
from .forms import LessonFilterForm, HomeworkFilterForm
# Create your views here.

class GetLessons(ListView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'daily_sys/daily.html'

    def get_lessons_data(self, **kwargs):   
        context = super().get_context_data(**kwargs)
        context["form"] = LessonFilterForm(self.request.GET)
        return context