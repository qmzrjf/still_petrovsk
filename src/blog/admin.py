from django.contrib import admin

from blog.models import User, Post, Category
from blog.forms import AdminPostForm


class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'username', 'is_active', 'avatar', 'author_status']


class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'text', 'author', 'picture', 'category']


class CategoryAdmin(admin.ModelAdmin):
    fields = ['category_name']


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
