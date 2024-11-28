from django.contrib import admin
from .models import Category, Topic, Comment, Like

admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Like)
