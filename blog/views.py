from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import BlogPost
from django.core.exceptions import PermissionDenied

# Create your views here.
def blog_list(request):
    """
    View to list all blog posts.
    """
    posts = BlogPost.objects.order_by('-created_at')

    if not request.user.is_staff:
        posts = posts.filter(status='published')
    return render(request, 'blog-list.html', {'posts': posts})


def blog_detail(request, slug):
    """
    View to display a single blog post.
    """
    post = get_object_or_404(BlogPost, slug=slug)

    if not request.user.is_staff and post.status == 'draft':
        raise PermissionDenied()

    return render(request, 'blog-detail.html', {'post': post})