from django.db import models
from django.core.exceptions import ValidationError

import re
# Create your models here.

def validate_id_number(value):
    """Validate SA ID numbers by checking length, DoB, citizenship, and gender digits"""
    id_number = str(value)

    if len(id_number) != 13:
        raise ValidationError(
            "The South African ID number must be 13 digits long."
            )
    
    if not id_number.isdigit():
        raise ValidationError(
            "The South African ID number must contain only digits."
            )
    
    year = int(id_number[0:2])
    month = int(id_number[2:4])
    day = int(id_number[4:6])

    if not (
        year >= 0 and year <= 99 and
        month >= 1 and month <= 12 and
        day >= 1 and day <= 31
        ):
        raise ValidationError(
            "Invalid birthdate in the South African ID number."
            )

    citizenship = int(id_number[10])
    if citizenship not in [0,1]:
        raise ValidationError(
            "Invalid citizen digit in the South African ID number."
            )
    
    gender = int(id_number[6])
    if gender not in [0,1,2,3]:
        raise ValidationError(
            "Invalid gender digit in South African ID number."
        )

    return value

def validate_phone_number(value):
    """Validate phone numbers by checking against common formats"""
    phone_number_regex = [
        r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
    ]

    if not any(re.match(regex, value) for regex in phone_number_regex):
        raise ValidationError(
            "Invalid phone number format"
        )

    return value

class iBuyProperty(models.Model):
    """Model for iBuy Property submissions"""
    full_name = models.CharField(
        null=False, blank=False,
        max_length=100,
        )
    id_number = models.PositiveIntegerField(
        null=False, blank=False, 
        validators=[validate_id_number],
        )
    phone_number = models.CharField(
        null=False, blank=False, 
        validators=[validate_phone_number],
        max_length=20,
        )
    email_address = models.EmailField(null=False, blank=False)
    address = models.CharField(
        null=False, blank=False, 
        max_length=150,
        )
    num_bedrooms = models.PositiveSmallIntegerField(null=False, blank=False)
    num_bathrooms = models.PositiveSmallIntegerField(null=False, blank=False)
    num_lounges = models.PositiveSmallIntegerField(null=False, blank=False)
    num_garages = models.PositiveSmallIntegerField(null=False, blank=False)
    expected_price = models.CharField(
        null=False, blank=False,
        max_length=50,
        )


def ibuy_image_upload_to(instance, filename):
    if isinstance(instance, iBuyImage):
        ibuy = instance.ibuy_submission
        folder = f"{ibuy.pk}"
    return f'ibuy_images/{folder}/{filename}'
    

class iBuyImage(models.Model):
    """Model for iBuy submission images"""
    ibuy_submission = models.ForeignKey(iBuyProperty, on_delete=models.CASCADE, default=None, related_name="ibuy_images")
    image = models.ImageField(upload_to=ibuy_image_upload_to, null=True, blank=True)
