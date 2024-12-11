from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum, name='forum'),
    path('category/', views.CategoryListView.as_view(), name='category'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('create-topic/', views.TopicCreateView.as_view(), name='create-topic'),
    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic-detail'),
    path('topic/<int:pk>/edit/', views.update_topic, name='update-topic'),
    path('create-poll/', views.create_poll, name='create-poll'),
    path('delete/<int:pk/', views.delete_topic, name='delete_topic'),
]