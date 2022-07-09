from django.contrib import admin

# Register your models here.
from .models import Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
