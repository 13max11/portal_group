from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import GalleryItem
from .forms import GalleryItemForm
from django.urls import reverse_lazy

# Create your views here.

def gallery(request):
    gallery_items = GalleryItem.objects.filter(verified=True)
    not_verified = GalleryItem.objects.filter(verified=False).count()
    context = {
        'gallery_items': gallery_items,
        'not_verified': not_verified,
    }

    return render(request, 'gallery_system/gallery.html', context)

class GalleryItemDeleteView(DeleteView):
    model = GalleryItem
    template_name = 'gallery_system/gallery.html'
    success_url = reverse_lazy('gallery')

    def get(self, request, *args, **kwargs):
        # Автоматичне видалення при GET запиті
        return self.post(request, *args, **kwargs)

class GalleryItemCreateView(CreateView):
    model = GalleryItem
    form_class = GalleryItemForm
    template_name = 'gallery_system/galleryitem_create.html'
    success_url = reverse_lazy('gallery')

    def form_valid(self, form):
        # Automatically set verified to True if the user is staff
        if self.request.user.is_staff:
            form.instance.verified = True
        return super().form_valid(form) 

def gallery_item_verification(request):
    if request.user.is_staff:
        gallery_items = GalleryItem.objects.filter(verified=False)
        context = {
            'gallery_items': gallery_items,
        }

        return render(request, 'gallery_system/verification.html', context)
    else:
        return redirect('gallery')

def gallery_item_verificate(request, pk):
    if request.user.is_staff:
        gallery_item = get_object_or_404(GalleryItem, pk=pk)

        gallery_item.verified = True
        gallery_item.save()

        return redirect('gallery')
    else:
        return redirect('gallery')