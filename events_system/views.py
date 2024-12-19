from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from .forms import EventForm
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Event

from django.utils import timezone

def event_list(request):
    events = Event.objects.filter(date_end__gte=timezone.now()).order_by('date_end')  
    return render(request, 'events_system/event_list.html', {'events': events})

class EventDetailsView(DetailView):
    model = Event
    template_name = 'events_system/event_details.html'

class EventCreateView(UserPassesTestMixin ,CreateView):
    form_class = EventForm
    template_name = 'events_system/event_create.html'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('index')

    def form_valid(self, form):
        form.instance.creation_date = timezone.now()
        self.object = form.save()
        return redirect('event-details', pk=self.object.pk)  # Перенаправляем на страницу с деталями топика