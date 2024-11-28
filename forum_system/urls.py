from django.urls import path
from . import views

urlpatterns = [
    path('category/<int:category_id>/', views.category_detail, name='category-detail'),
    path('category/<int:category_id>/create-topic/', views.create_topic, name='create-topic'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic-detail'),
]