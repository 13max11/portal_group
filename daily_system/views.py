from django.shortcuts import render
from .models import Lesson
from django.views.generic import ListView
from .forms import LessonFilterForm, HomeworkFilterForm
from django.urls import reverse_lazy
# Create your views here.

class LessonsListView(ListView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'daily_sys/daily.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):   
        context = super().get_context_data(**kwargs)
        context["form"] = LessonFilterForm(self.request.GET)
        return context
    
class HomeworkListView(ListView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'daily_sys/homework_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):   
        context = super().get_context_data(**kwargs)
        context["form"] = HomeworkFilterForm(self.request.GET)
        return context
    
    def homework_details(self, request, pk):
        homework = Lesson.objects.get(id=pk)
        context = {
            'homework': homework
      }

        return render(request, 'daily_sys/homework_detail.html', context)