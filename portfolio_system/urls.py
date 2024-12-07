from django.urls import path
from . import views

urlpatterns = [
    path('projects/<int:pk>/', views.project_details, name='project-detail'),
]