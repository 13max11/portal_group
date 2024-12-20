from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum, name='forum'),
    path('category/', views.CategoryListView.as_view(), name='category'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('create-topic/', views.topic_create_view, name='create-topic'),
    path('create-topic/<int:pk>', views.topic_create_category, name='create-topic'),
    path('category/create/', views.create_category, name='create-category'),
    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic-detail'),
    path('topic/<int:pk>/edit/', views.update_topic, name='update-topic'),
    path('topic/<int:pk>/delete/', views.delete_topic, name='delete-topic'),

    # urls для голосування
    path('poll/<int:pk>/vote/', views.vote_poll, name='vote'),
    path('topic/<int:topic_id>/create-poll/', views.create_poll, name='create-poll'),
    path('poll/<int:poll_id>/delete/', views.delete_poll, name='delete-poll'),
    path('poll/<int:poll_id>/add-option/', views.add_poll_option, name='add-poll-option'),
    path('poll-option/<int:option_id>/delete/', views.delete_poll_option, name='delete-poll-option'),
]