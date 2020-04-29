from django.contrib import admin

from blog.models import User, Post
from blog.forms import AdminPostForm


class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'username', 'is_active', 'avatar']


class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'text', 'author', 'picture']


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
