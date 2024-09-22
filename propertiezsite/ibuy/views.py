from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage


from .forms import iBuyPropertyForm
from .models import iBuyImage

# Create your views here.
def draft_email(ibuy):
    subject = "New iBuy submission"
    email = f"""
A new iBuy Property has been submitted to the site.
Here are the details:

Full Name: {ibuy.full_name}
ID Number: {ibuy.id_number}
Phone Number: {ibuy.phone_number}
Email Address: {ibuy.email_address}
Address: {ibuy.address}
No. Bedrooms: {ibuy.num_bedrooms}
No. Bathrooms: {ibuy.num_bathrooms}
No. Lounges: {ibuy.num_lounges}
No. Garages: {ibuy.num_garages}
Expected Price: {ibuy.expected_price}

This is an automated email, if you have any queries or concerns, please contact us at care@propertiez.co.za
"""
    
    return subject, email

def send_ibuy_email(ibuy, files):
    subject, message = draft_email(ibuy)
    from_email = "enquiry@propertiez.co.za"
    if ibuy.full_name.lower() == 'test':
        recipiant_list = ['michaela@propertiez.co.za']
    else:
        recipiant_list = ['care@propertiez.co.za']
    
    email = EmailMessage(subject, message, from_email, recipiant_list)
    for file in files:
        file.seek(0)
        email.attach(file.name, file.read(), file.content_type)
        file.close()
    email.send()
    

def add_ibuy(request):
    if request.method == 'POST':
        form = iBuyPropertyForm(request.POST)
        files = request.FILES.getlist('ibuy-image')

        if form.is_valid():
            ibuy = form.save()

            images = []
            for file in files:
                image = iBuyImage.objects.create(ibuy_submission=ibuy, image=file)
                images.append(image)

            send_ibuy_email(ibuy, files)

            if ibuy.full_name.lower() == "test":
                ibuy.delete()
            
            messages.success(request, "iBuy application submitted successfully!")
        else:
            messages.error(request, "Invalid form")
    else:
        form = iBuyPropertyForm()
    
    return render(request, 'apply.html', {'form': form})