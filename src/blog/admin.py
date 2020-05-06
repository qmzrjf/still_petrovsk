from django.contrib import admin

from blog.models import User, Post, Category
from blog.forms import AdminPostForm


class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'username', 'is_active', 'avatar', 'author_status', 'groups', 'is_staff']


class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'text', 'author', 'picture', 'category']

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.author != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.author != request.user:
            return False
        return True


class CategoryAdmin(admin.ModelAdmin):
    fields = ['category_name']


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
