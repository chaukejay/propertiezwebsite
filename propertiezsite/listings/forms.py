from django import forms
from .models import ResidentialListing, ListingImage, ListingEnquiry


class ListingImageForm(forms.ModelForm):
    class Meta:
        model = ListingImage
        fields = ['image']



class ResidentialListingForm(forms.ModelForm):
    class Meta:
        model = ResidentialListing
        fields = [
            "agent",

            "street_number", "street_name", "publish_street_address",
            "suburb", "area", "city", "province", "post_code",

            "status", "price", "listing_type",
            
            "bedrooms", "bathrooms",
            "studies", "lounges", "dining_rooms",
            "garages", "carports",

            "property_type", "description", 
            "floor_size", "floor_size_measurement_type",
            "land_size", "land_size_measurement_type",

            "main_image"
            ]


class ListingEnquiryForm(forms.ModelForm):
    class Meta:
        model = ListingEnquiry
        fields = [
            "full_name", "email", "cell_number", "is_prequalified", "message",
            "add_to_mailing_list", "consent_information",
            "consent_messages", "consent_calls"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].required = True
        self.fields['email'].required = True
        self.fields['consent_information'].required = True
        self.fields['consent_messages'].required = True