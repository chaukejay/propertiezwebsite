from django.db import models
from django.core.validators import MinValueValidator
from django.core import validators
from agents.models import Agent


# Create your models here.
class PropDataIntegration(models.Model):
    agent_id = models.PositiveIntegerField(null=False, blank=False)
    branch_id = models.PositiveIntegerField(null=False, blank=False)
    location_id = models.PositiveIntegerField(null=False, blank=False)
    area_id = models.PositiveIntegerField(null=False, blank=False)


def listing_image_upload_to(instance, filename):
    # Construct the upload path based on the listing ID
    if isinstance(instance, ResidentialListing):
        listing = instance
    elif isinstance(instance, ListingImage):
        listing = instance.residential_listing
    else:
        return 'listing_images/unknown/'
    "media/listing_images/123_StreetName_SurburbName_AreaName/sample-1.jpg"
    listing_folder = f"{listing.street_number}_{listing.street_name}_{listing.suburb}_{listing.area}"
    return f'listing_images/{listing_folder}/{filename}'


class ResidentialListing(models.Model):
    """Model for Residential Listings."""
    STATUSES = [
        ("Active", "Active"), ("Pending", "Pending"), ("Rented", "Rented"),
        ("Sold", "Sold"), ("Archived", "Archived"), ("Valuation", "Valuation")
    ]
    LISTING_TYPES = [
        ("For Sale", "For Sale"), ("To Let", "To Let")
    ]
    PROPERTY_TYPES = [
        ("Apartment Block", "Apartment Block"),
        ("Apartment", "Apartment"),
        ("Bed & Breakfast", "Bed & Breakfast"),
        ("Building", "Building"),
        ("Bungalow", "Bungalow"),
        ("Club", "Club"),
        ("Cluster", "Cluster"),
        ("Commercial", "Commercial"),
        ("Compound", "Compound"), 
        ("Detached", "Detached"),
        ("Duet", "Duet"),
        ("Duplex", "Duplex"), 
        ("Equestrian Property", "Equestrian Property"),
        ("Farm", "Farm"), 
        ("Flat", "Flat"),
        ("Freehold", "Freehold"),
        ("Freestanding", "Freestanding"),
        ("Full Floor", "Full Floor"),
        ("Garden Cottage", "Garden Cottage"),
        ("Gated Estate", "Gated Estate"),
        ("Golf Estate", "Golf Estate"),
        ("Guest House", "Guest House"),
        ("Half Floor", "Half Floor"),
        ("Hotel Room", "Hotel Room"),
        ("Hotel", "Hotel"),
        ("House", "House"),
        ("Industrial", "Industrial"),
        ("Labour Camp", "Labour Camp"),
        ("Leaseback", "Leaseback"),
        ("Lodge", "Lodge"),
        ("Maisonette", "Maisonette"),
        ("Office", "Office"),
        ("Package Home", "Package Home"),
        ("Penthouse", "Penthouse"),
        ("Retirement Unit", "Retirement Unit"),
        ("Room", "Room"),
        ("Sectional Title", "Sectional Title"),
        ("Semi Detached", "Semi Detached"),
        ("Simplex", "Simplex"),
        ("Small Holding", "Small Holding"),
        ("Studio Apartment", "Studio Apartment"),
        ("Townhouse", "Townhouse"),
        ("Vacant Land", "Vacant Land"),
        ("Villa", "Villa"),
        ("Warehouse", "Warehouse")
    ]
    FLOOR_SIZE_MEASUREMENT_TYPE = [
        ("Square Metres", "Square Metres"), ("Square Feet", "Square Feet")
    ]
    LAND_SIZE_MEASUREMENT_TYPE = [
        ("Square Metres", "Square Metres"), ("Hectares", "Hectares"),
        ("Square Feet", "Square Feet"), ("Acres", "Acres")
    ]
    PROVINCES = [
        ("Eastern Cape", "Eastern Cape"), ("Free State", "Free State"),
        ("Gauteng", "Gauteng"), ("KwaZulu-Natal", "KwaZulu-Natal"),
        ("Limpopo", "Limpopo"), ("Mpumalanga", "Mpumalanga"),
        ("Northern Cape", "Northern Cape"), ("North West", "North West"),
        ("Western Cape", "Western Cape")
    ]
    model = "Residential"
    
    # Property Details
    description = models.TextField(null=True, blank=False)
    status = models.CharField(null=False, blank=False, choices=STATUSES, max_length=20)
    price = models.DecimalField(null=True, blank=False, decimal_places=2, validators=[MinValueValidator(0)], max_digits=20)
    listing_type = models.CharField(null=False, blank=False, choices=LISTING_TYPES, max_length=20)
    property_type = models.CharField(null=False, blank=False, choices=PROPERTY_TYPES, max_length=50)
    # Area
    floor_size = models.DecimalField(null=True, blank=True, decimal_places=2, validators=[MinValueValidator(0)], max_digits=20)
    floor_size_measurement_type = models.CharField(null=True, blank=True, choices=FLOOR_SIZE_MEASUREMENT_TYPE, max_length=20)
    land_size = models.DecimalField(null=True, blank=True, decimal_places=2, validators=[MinValueValidator(0)], max_digits=20)
    land_size_measurement_type = models.CharField(null=True, blank=True, choices=LAND_SIZE_MEASUREMENT_TYPE, max_length=20)
    # Agent
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    # Location
    street_number = models.CharField(null=True, blank=False, max_length=10)
    street_name = models.CharField(null=True, blank=False, max_length=100)
    publish_street_address = models.BooleanField(default=True)
    suburb = models.CharField(null=True, blank=True, max_length=100)
    area = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(null=True, blank=False, max_length=100)
    province = models.CharField(null=True, blank=False, choices=PROVINCES, max_length=100)
    post_code = models.PositiveIntegerField(null=True, blank=True)

    # Rooms
    bedrooms = models.DecimalField(
        null=True, blank=True, decimal_places=1, default=0,
        validators=[MinValueValidator(0)], max_digits=6
    )
    bathrooms = models.DecimalField(
        null=True, blank=True, decimal_places=1, default=0,
        validators=[MinValueValidator(0)], max_digits=6
    )
    studies = models.DecimalField(
        null=True, blank=True, decimal_places=1, default=0,
        validators=[MinValueValidator(0)], max_digits=6)
    lounges = models.DecimalField(
        null=True, blank=True, decimal_places=1, default=0,
        validators=[MinValueValidator(0)], max_digits=6
    )
    dining_rooms = models.DecimalField(
        null=True, blank=True, decimal_places=1, default=0,
        validators=[MinValueValidator(0)], max_digits=6
    )
    garages = models.DecimalField(
        null=True, blank=True, decimal_places=1, default=0,
        validators=[MinValueValidator(0)], max_digits=6
    )
    carports = models.DecimalField(
        null=True, blank=True, decimal_places=1, default=0,
        validators=[MinValueValidator(0)], max_digits=6)
    
    # Images
    main_image = models.ImageField(upload_to=listing_image_upload_to, null=True, blank=True)
    # Metadata
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)

    """
    deleted: nullable datetime yyyy-mm-ddThh:mm:ss.SSSZ

    """
    

    def __str__(self):
        """String representation of a Residential Listing."""
        locations = []
        if self.suburb:
            locations.append(self.suburb)
        if self.area:
            locations.append(self.area)
        if self.city:
            locations.append(self.city)
        if self.province:
            locations.append(self.province)
        location = ", ".join(locations)

        bedrooms = ""
        if self.bedrooms:
            bedrooms += str(self.bedrooms.normalize()) + " Bedroom "
        return bedrooms + self.property_type + " " + self.listing_type + " in " + location


class ListingImage(models.Model):
    """Model for additional listing images"""
    residential_listing = models.ForeignKey(ResidentialListing, on_delete=models.CASCADE, default=None, related_name="listing_images")
    image = models.ImageField(upload_to=listing_image_upload_to, null=True, blank=True)

    def __str__(self):
        return self.image.name
    

class ListingFloorplan(models.Model):
    """Model for listing floorplans"""
    image = models.ImageField(upload_to=listing_image_upload_to, null=True, blank=True)


class ListingEnquiry(models.Model):
    """Model for Listing Enquiries."""
    """
    Properties fetched from Listing:
    branch_id <- listing.branch
    listing_model <- listing.model
    listing type <- listing.listing_type:
            { "For Sale": "Buyer",
              "To Let": "Tenant" }
    agent_id <- listing.agent
    areas <- ADD listing.area
    suburbs <- ADD listing.suburb
    property_type <- listing.property_type
    property_types <- ADD listing.property_type
    bedrooms <- listing.bedrooms
    bathrooms <- listing.bathrooms
    garages <- listing.garages
    carports <- listing.carports
    asking_price <- listing.price
    property_address <- listing.street_number + " " + listing.street_name
    property_description <- listing.description
    """
    # Visible Fields
    full_name = models.CharField(null=False, blank=False, max_length=100)
    email = models.EmailField(null=False, blank=False)
    cell_number = models.CharField(null=True, blank=True, max_length=10)
    message = models.TextField(null=True, blank=True, default="Hi, I'm interested in learning more about this property.")
    
    # Propdata stuff
    propdata_id = models.BigIntegerField(null=True, blank=True)
    source = models.CharField(null=False, blank=False, default="Propertiez.co.za", max_length=30)
    source_ref = models.CharField(blank=False, default="e36ef6e1-be37-44ca-94d1-3308b7905b8d", max_length=100)
    source_description = models.CharField(null=False, blank=True, default="Portal", max_length=100)
    hubspotutk = models.CharField(null=True, blank=True, max_length=100)
    
    # Agent, Branch, Listing details
    # branch_id: int, required
    # agent_id: int, nullable
    listing = models.ForeignKey(ResidentialListing, null=False, blank=False, on_delete=models.CASCADE)
    asking_price = models.PositiveIntegerField(null=True, blank=True)
    zoning = models.CharField(max_length=50, blank=True)
    # listing_model: string, nullable, choice: [“Residential”, “Commercial”, “Project”, “Holiday”]
    # listing_type: string, nullable, choice [“Buyer”, “Tenant”]
    # property_type: string, nullable
    # bedrooms: string decimal, nullable
    # bathrooms: string decimal, nullable
    # garages: string decimal, nullable
    # carports: string decimal, nullable
    # property_address: string, nullable
    # property_description: string, nullable
    
    # Additional Info
    page_url = models.CharField(null=True, blank=True, max_length=200)
    user_types = models.JSONField(null=True, blank=True, default=list)
    areas = models.JSONField(null=True, blank=True, default=list)
    suburbs = models.JSONField(null=True, blank=True, default=list)
    property_types = models.JSONField(null=True, blank=True, default=list)
    price_from = models.PositiveIntegerField(null=True, blank=True)
    price_to = models.PositiveIntegerField(null=True, blank=True)

    size_from = models.PositiveIntegerField(null=True, blank=True)
    size_to = models.PositiveIntegerField(null=True, blank=True)
    floor_size_from = models.PositiveIntegerField(null=True, blank=True)
    floor_size_to = models.PositiveIntegerField(null=True, blank=True)
    erf_size_from = models.PositiveIntegerField(null=True, blank=True)
    erf_size_to = models.PositiveIntegerField(null=True, blank=True)

    subscribe_date = models.DateTimeField(null=True, blank=True) # yyyy-mm-ddThh:mm:ss.SSSZ
    unsubscribe_date = models.DateTimeField(null=True, blank=True) # yyyy-mm-ddThh:mm:ss.SSSZ

    is_prequalified = models.BooleanField(default=False)

    # Consent and POPIA stuff
    legal_basis = models.CharField(null=True, blank=False, max_length=200)
    status = models.CharField(null=True, default="no_consent", max_length=100)
    add_to_mailing_list = models.BooleanField(default=False, blank=True)
    add_to_profiles = models.BooleanField(default=False, blank=True)
    add_to_leads = models.BooleanField(default=False, blank=True)
    consent_messages = models.BooleanField(default=False, blank=True)
    consent_messages_subscribe_date = models.DateTimeField(null=True, blank=True) # yyyy-mm-ddThh:mm:ss.SSSZ
    consent_messages_unsubscribe_date = models.DateTimeField(null=True, blank=True) # yyyy-mm-ddThh:mm:ss.SSSZ
    consent_calls = models.BooleanField(default=False, blank=True)
    consent_calls_subscribe_date = models.DateTimeField(null=True, blank=True) # yyyy-mm-ddThh:mm:ss.SSSZ
    consent_calls_unsubscribe_date = models.DateTimeField(null=True, blank=True) # yyyy-mm-ddThh:mm:ss.SSSZ
    consent_information = models.BooleanField(default=False, blank=True)
    

