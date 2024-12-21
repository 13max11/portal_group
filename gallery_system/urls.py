from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('create/', views.GalleryItemCreateView.as_view(), name='gallery-create'),
    path('verification/', views.gallery_item_verification, name='gallery-verification'),
    path('verification/<int:pk>/', views.gallery_item_verificate, name='gallery-verificate'),
    path('<int:pk>/delete/', views.gallery_item_delete, name='gallery-delete'),
]