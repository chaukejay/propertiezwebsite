from django.contrib import admin
from .models import iBuyProperty, iBuyImage

# Register your models here.
admin.site.register([iBuyProperty, iBuyImage])