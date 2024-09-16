from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms

from .forms import ResidentialListingForm, ListingImageForm, ListingEnquiryForm
from .models import ResidentialListing, ListingImage


# Create your views here.
@login_required
def add_listing(request):
    if not request.user.is_staff:
        messages.warning(request, "Only Staff may access this page")
        return render(request, 'access-denied.html')

    if request.method == 'POST':
        form = ResidentialListingForm(request.POST, request.FILES)
        files = request.FILES.getlist('listing-image')

        if form.is_valid():
            listing = form.save()
            # Handle listing images
            for file in files:
                ListingImage.objects.create(residential_listing=listing, image=file)
            
            return redirect("listing-details", pk=listing.pk)
        
        else:
            messages.error(request, "Invalid form")

    else:
        form = ResidentialListingForm()

    return render(request, 'add-listing.html', {'form': form})


@login_required
def edit_listing(request, pk):
    if not request.user.is_staff:
        messages.warning(request, "Only Staff may access this page")
        return render(request, 'access-denied.html')

    ListingImageFormSet = forms.modelformset_factory(ListingImage, form=ListingImageForm)

    listing = get_object_or_404(ResidentialListing, pk=pk)

    if request.method == 'POST':
        form = ResidentialListingForm(request.POST, request.FILES, instance=listing)
        # Existing Images
        image_queryset = ListingImage.objects.filter(residential_listing=listing)
        image_formset = ListingImageFormSet(request.POST, request.FILES, queryset=image_queryset)
        # New Images
        files = request.FILES.getlist('listing-image')


        if form.is_valid() and image_formset.is_valid():
            listing = form.save(commit=False)
            print(listing)
            image_instances = image_formset.save(commit=False)

            for image_instance in image_instances:
                if not image_instance.pk and not image_instance.image:
                    # If the image instance is new and the image field is empty, skip it
                    continue
                image_instance.residential_listing = listing
                image_instance.save()

            for image_form in image_formset.deleted_forms:
                if image_form.instance.pk:
                    image_form.instance.delete()
            
            listing.save()
            image_formset.save()

            for file in files:
                ListingImage.objects.create(residential_listing=listing, image=file)

            return redirect('listing-details', pk=listing.pk)

    else:
        # fill the form with the listing data
        form = ResidentialListingForm(instance=listing)
        # fetch the images associated to the listing
        image_queryset = ListingImage.objects.filter(residential_listing=listing)
        # fill the image formset with the listing images
        image_formset = ListingImageFormSet(queryset=image_queryset)


    return render(request, 'edit-listing.html', {'form': form, 'image_formset': image_formset})
    

def handle_consent(enquiry):
    timezone.activate(timezone.get_current_timezone())
    current_time = timezone.now()
    
    status = ""
    if enquiry.consent_information:
        status = status + "consent_information "
    if enquiry.consent_messages:
        enquiry.consent_messages_subscribe_date = current_time
        status = status + "consent_messages "
    if enquiry.consent_calls:
        enquiry.consent_calls_subscribe_date = current_time
        status = status + "consent_calls "
    # contact number given with no consent given
    if not enquiry.consent_calls and enquiry.cell_number:
        # scrub the number
        enquiry.cell_number = None
    enquiry.status = status

    return enquiry
    

def draft_enquiry_email(enquiry):
    subject = f"New Enquiry for: {enquiry.listing}"
    # a if a<b else b
    email = f"""
Hi, you have received a new enquiry from {enquiry.full_name},

Contact Details:
    Email: {enquiry.email}
    {"Contact Number: " + enquiry.cell_number if enquiry.consent_calls and enquiry.cell_number else ""}

Users message:
{enquiry.message}

User has pre-qualified for a home loan?
{"Yes" if enquiry.is_prequalified else "No"}

User Consent Details:
    Consent given for information storage, processing and sharing for the purpose of getting information about this listing? 
    {"Yes" if enquiry.consent_information else "No"}
    Consent given for email communication with regard to this listing? 
    {"Yes" if enquiry.consent_messages else "No"}
    Consent given for telephonic communication with regard to this listing? 
    {"Yes" if enquiry.consent_calls else "No"}

Listing Details:
    Listing: {enquiry.listing}
    Page Url: {enquiry.page_url}
    Current Asking Price: R{enquiry.asking_price}
    Description: {enquiry.listing.description}

This is an automated email, if you have any queries or concerns, please contact us at care@propertiez.co.za
    """
    return subject, email


def send_enquiry_to_agent(request, enquiry):
    subject, message = draft_enquiry_email(enquiry)
    from_email = "enquiry@propertiez.co.za"
    internal_recipiants = [
        'abigail@propertiez.co.za',
        'enquiry@propertiez.co.za'
        ]

    test_email = True if enquiry.full_name.lower() == 'test' else False
    if test_email:
        recipiant_list = ['michaela@propertiez.co.za']
    else:
        recipiant_list = [enquiry.listing.agent.email]

    try:
        result = send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipiant_list, fail_silently=False)
        if not test_email:
            result = send_mail(subject=subject, message=message, from_email=from_email, recipient_list=internal_recipiants, fail_silently=False)
    except Exception as e:
        messages.error(request, "Failed to send enquiry, please try again or contact us for support")
        print("Error sending email ", e)
    else:
        messages.success(request, "Enquiry sent!")


def listing_details(request, pk):
    listing = get_object_or_404(ResidentialListing, pk=pk)
    listing_images = listing.listing_images.all()
    # image = listing.main_image.open()
    # print(image)

    if request.method == 'POST':
        form = ListingEnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            # Addtional fields
            enquiry.listing = listing
            enquiry.legal_basis = "User submitted enquiry regarding property listing, information stored, processed and shared to facilitate connection between user and agent"
            enquiry.page_url =  f"propertiez.co.za{reverse('listing-details', kwargs={'pk': listing.id})}"
            enquiry.asking_price = listing.price

            user_types = []
            if listing.listing_type == "For Sale":
                user_types.append("Buyer")
            if listing.listing_type == "To Let":
                user_types.append("Tenant")
            enquiry.user_types = user_types
            
            enquiry = handle_consent(enquiry)

            send_enquiry_to_agent(request, enquiry)

            # equiry.field = "value"
            if enquiry.full_name.lower() != "test":
                enquiry.save()

    else:
        form = ListingEnquiryForm()

        # Handle view counter

        if not request.user.is_staff:
            num_views = listing.view_count
            print("old views: ", num_views)
            num_views += 1
            listing.view_count = num_views
            listing.save()
            print("new views: ", listing.view_count)

    return render(request, 'listing-details.html', {'listing': listing, 'listing_images': listing_images, "form":form})


def get_values_list(queryset, field_name):
    return queryset.order_by(field_name).values_list(field_name, flat=True).distinct()


def get_dropdown_options(queryset):
    LISTING_TYPES = get_values_list(queryset, 'listing_type')
    PROPERTY_TYPES = get_values_list(queryset, 'property_type')
    SUBURBS = get_values_list(queryset, 'suburb')
    AREAS = get_values_list(queryset, 'area')
    CITIES = get_values_list(queryset, 'city')
    PROVINCES = get_values_list(queryset, 'province')

    options = {
        "listing_type_options": LISTING_TYPES,
        "property_type_options": PROPERTY_TYPES,
        "suburb_options": SUBURBS,
        "area_options": AREAS,
        "city_options": CITIES,
        "province_options": PROVINCES
    }
    return options


def search_listings(request):
    model = "Residential"
    # match model:
    #     case "Residential":
    #         # get res query set
    #         queryset = ResidentialListing.objects.all()
    #     case "Commercial":
    #         # get com query set
    #         # queryset = CommercialListing.objects.all()
    #         pass
    #     case "Development":
    #         # get dev query set
    #         # queryset = ProjectListing.objects.all()
    #         pass
    #     case _:
    #         # get all listings
    #         queryset = ResidentialListing.objects.all()
    # PROPERTY_TYPES = ResidentialListing.objects.order_by('property_type').values_list('property_type', flat=True).distinct()

    # Fetch all properties
    queryset = ResidentialListing.objects.all()
    # Filter to active properties only
    queryset = queryset.filter(status='Active')

    options = get_dropdown_options(queryset)

    # Filter by listing type
    listing_type = request.GET.get('listing_type')
    if listing_type:
        queryset = queryset.filter(listing_type=listing_type)

    # Filter by location
    suburb = request.GET.get('suburb')
    if suburb:
        queryset = queryset.filter(suburb__icontains=suburb)
    area = request.GET.get('area')
    if area:
        queryset = queryset.filter(area__icontains=area)
    city = request.GET.get('city')
    if city:
        queryset = queryset.filter(city__icontains=city)
    province = request.GET.get('province')
    if province:
        queryset = queryset.filter(province__icontains=province)

    # Filter by property type (select multiple)
    property_types = request.GET.getlist('property_type')
    if property_types:
        queryset = queryset.filter(property_type__in=property_types)

    # Filter by price
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        queryset = queryset.filter(price__gte=price_min)
    if price_max:
        queryset = queryset.filter(price__lte=price_max)
    
    # Filter by rooms
    bedrooms = request.GET.get('bedrooms')
    if bedrooms:
        queryset = queryset.filter(bedrooms__gte=bedrooms)
    bathrooms = request.GET.get('bathrooms')
    if bathrooms:
        queryset = queryset.filter(bathrooms__gte=bathrooms)

    # Paginate the queryset
    paginator = Paginator(queryset[::-1], 10) # Show 20 listings per page
    page = request.GET.get('page')

    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)

    return render(request, 'search-listings.html', {'listings': listings, 'options': options, 'model': model})


def listing_enquiry(request): 
    if request.method == 'POST':
        form = ListingEnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            # Addtional fields
            # equiry.field = "value"
            enquiry.save()

    else:
        form = ListingEnquiryForm()
    return render(request, 'enquiry-form.html', {"form": form})


def draft_fsbo_email(title, description, price, location, name, email, contact):
    return f"""
A new property listing request has been submitted with the following details:

Property Title: {title}

Description:
{description}
Price: R{price}

Location: {location}

Owner's Details:
Name: {name}
Email: {email}
Contact Number: {contact}

Please review the details and proceed with the necessary actions.
"""


def fsbo_application(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        location = request.POST['location']
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']

        recipients = ['care@propertiez.co.za']
 
        # print()

        subject = f"New Property Listing Request - {title}"
        message = draft_fsbo_email(title, description, price, location, name, email, contact)

        try:
            send_mail(subject, message, email, recipients)
        except Exception as e:
            print("Error sending contact message: ", e)
            messages.error(request, "Failed to submit application, please try again or contact us at care@propertiez.co.za")
        else:
            messages.success(request, "Application submitted")
    return render(request, 'fsbo-application.html')

        



    


    