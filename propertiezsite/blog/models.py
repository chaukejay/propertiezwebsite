from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
# Create your models here.

def blog_image_upload_to(blogpost, filename):
    return f"blogpost_images/{blogpost.slug}/{filename}"

class BlogPost(models.Model):
    """
    Model representing a blog post.
    """
    STATUSES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=100, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to=blog_image_upload_to, null=True, blank=True, default=None)

    excerpt = models.TextField(max_length=200, blank=True)

    slug = models.SlugField(max_length=200, unique=True, blank=True)
    tags = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUSES, default='draft')

    created_at = models.DateTimeField(default=timezone.now)
    uploaded_at = models.DateTimeField(auto_now=True)
    

    def save(self, *args, **kwargs):
        """
        Override save method to automatically generete slug from title if not
        provided.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
    

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"


