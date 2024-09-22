from django.contrib import admin
from .models import ResidentialListing, ListingEnquiry, ListingImage

# Register your models here.
admin.site.register([ListingEnquiry, ListingImage])

@admin.register(ResidentialListing)
class ResidentialListingAdmin(admin.ModelAdmin):
    readonly_fields = ('view_count',)