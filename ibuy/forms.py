from django import forms
from .models import iBuyProperty, iBuyImage


class iBuyPropertyForm(forms.ModelForm):
    class Meta:
        model = iBuyProperty
        fields = [
            "full_name", "id_number", "phone_number",
            "email_address", "address", "num_bedrooms",
            "num_bathrooms", "num_lounges", "num_garages",
            "expected_price"
        ]
        labels = {
            "id_number": "ID number",
            "num_bedrooms": "No. Bedrooms",
            "num_bathrooms": "No. Bathrooms",
            "num_lounges": "No. Lounges",
            "num_garages": "No. Garages",
            "num_bedrooms": "No. Bedrooms",

        }


class iBuyImageForm(forms.ModelForm):
    class Meta:
        model = iBuyImage
        fields = ['image']