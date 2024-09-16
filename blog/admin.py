from django.contrib import admin
from .models import BlogPost
from django import forms

# Register your models here.
# class BlogPostAdminForm(forms.ModelForm):

#     class Meta:
#         model = BlogPost
#         fields = '__all__'


class BlogPostAdmin(admin.ModelAdmin):
    """
    Admin configuration for the BlogPost model.
    """
    # form = BlogPostAdminForm
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'author')
    search_fields = ('title', 'author__username', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('status','-created_at',)


admin.site.register(BlogPost, BlogPostAdmin)