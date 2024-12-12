from django.contrib import admin
from .models import Category, Topic, Comment, Like, Poll, PollOption, PollVote

admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Like)

admin.site.register(Poll)
admin.site.register(PollOption)
admin.site.register(PollVote)