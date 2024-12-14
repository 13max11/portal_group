from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetLessons.as_view(), name='daily'),
]