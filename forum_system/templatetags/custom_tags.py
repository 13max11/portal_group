# templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def has_voted(poll, user):
    return poll.votes.filter(user=user).exists()