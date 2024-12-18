from django.urls import path
from . import views

urlpatterns = [
    path('', views.GalleryListView.as_view(), name='gallery'),
    path('create/', views.GalleryItemCreateView.as_view(), name='gallery-create'),
    path('<int:pk>/delete/', views.GalleryItemDeleteView.as_view(), name='gallery-delete'),
]