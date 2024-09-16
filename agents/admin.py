from django.contrib import admin
from .models import Agent, Agency, Tag

# Register your models here.
admin.site.register([Agent, Agency, Tag])