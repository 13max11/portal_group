from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='events-list'),
    path('<int:pk>/', views.EventDetailsView.as_view(), name='event-details'),
    path('create', views.EventCreateView.as_view(), name='event-create'),
]