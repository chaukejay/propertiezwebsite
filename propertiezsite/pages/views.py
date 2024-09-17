from django.shortcuts import render
from listings.models import ResidentialListing
from listings.views import get_dropdown_options
from blog.models import BlogPost
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.

def about(request):
    """View function for the about page."""

    return render(request, 'about.html')


def calculators(request):
    """View function for the calculators page."""

    return render(request, 'calculators.html')


def draft_email(name, from_email, subject, message):
    return f"""
New Contact Form Submission

Name: {name}
Email: {from_email}
Subject: {subject}
Message:
{message}
"""


def contact_us(request):
    """View function for the contact us page."""
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        recipients = ['care@propertiez.co.za']

        print(name, email, subject, message, sep="\n")

        email_body = draft_email(name, email, subject, message)

        print(email_body)

        if name.lower() != 'test':
            try:
                send_mail(subject, email_body, email, recipients)
            except Exception as e:
                messages.error(request, "Failed to send message, please try again or contact us at care@propertiez.co.za for support")    
                print("Error sending contact message: ", e)
            else:
                messages.success(request, "Message sent!")
    return render(request, 'contact-us.html')


def error(request):
    """View function for the error page."""

    return render(request, 'error.html')


def faq(request):
    """View function for the FAQ page."""

    return render(request, 'faq.html')


def home_loans(request):
    """View function for the home loans page."""

    return render(request, 'home-loans.html')


def home(request):
    """View function for the home page."""
    # Fetch all listings
    listings = ResidentialListing.objects.all()
    # Filter to active listings only
    listings = listings.filter(status='Active')

    options = get_dropdown_options(listings)

    # show 20 most recent listings, sorted newest to oldest
    listings = listings[::-1]
    listings = listings[:20]

    # Fetch all blog posts
    posts = BlogPost.objects.all()
    # Filter to published
    if not request.user.is_staff:
        posts = posts.filter(status='published')
    # Show 20 most recent posts
    posts = posts[:20]

    return render(request, 'home.html', {'listings': listings, 'options': options, 'posts': posts})


def index(request):
    """View function for the index page."""

    return render(request, 'index.html')


def meet_the_team(request):
    """View function for the meet the team page."""

    return render(request, 'meet-the-team.html')


def privacy_policy(request):
    """View function for the privacy policy page."""

    return render(request, 'privacy-policy.html')


def services(request):
    """View function for the services page."""

    return render(request, 'services.html')


def terms_of_service(request):
    """View function for the terms of service page."""

    return render(request, 'terms-of-service.html')


def access_denied(request):
    """View function for the access denied page."""

    return render(request, 'access-denied.html')


def terms_and_conditions(request):
    """View function for the terms and conditions page."""

    return render(request, 'terms-and-conditions.html')


def cookie_policy(request):
    """View function for the cookie policy page."""

    return render(request, 'cookie-policy.html')

def sell(request):
    """View function for the sell page."""

    return render(request, 'sell.html')