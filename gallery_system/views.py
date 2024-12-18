from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import GalleryItem
from .forms import GalleryItemForm
from django.urls import reverse_lazy

# Create your views here.

class GalleryListView(ListView):
    model = GalleryItem
    template_name = 'gallery_system/gallery.html'
    context_object_name = 'gallery_items'

class GalleryItemDeleteView(DeleteView):
    model = GalleryItem
    template_name = 'gallery_system/gallery.html'
    success_url = reverse_lazy('gallery')

    def get(self, request, *args, **kwargs):
        # Автоматичне видалення при GET запиті
        return self.post(request, *args, **kwargs)

class GalleryItemCreateView(UserPassesTestMixin, CreateView):
    form_class = GalleryItemForm
    template_name = 'gallery_system/galleryitem_create.html'
    success_url = reverse_lazy('gallery')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')