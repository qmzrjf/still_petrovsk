from django.contrib import admin

from blog.models import User, Post, Category, Tag
from blog.forms import AdminPostForm


class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'username', 'is_active', 'avatar', 'author_status', 'groups', 'is_staff']


class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'text', 'author', 'picture', 'category', 'tags']

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


class TagAdmin(admin.ModelAdmin):
    fields = ['title']


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
