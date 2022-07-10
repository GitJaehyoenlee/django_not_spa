# https://docs.djangoproject.com/en/4.0/howto/custom-template-tags/
from django import template

register = template.Library()

@register.filter
def is_like_user(post, user):
    return post.is_like_user(user)