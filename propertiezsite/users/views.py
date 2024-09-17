from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm


def register(request):
    """View function for user registration."""

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Registration successful, welcome {username}!") #TODO ADD USERNAME HERE
            return redirect('login')
        else:
            form = CustomUserCreationForm(request.POST)
            messages.error(request, "Registration failed")
            return render(request, 'registration.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})


def user_login(request):
    """View function for user login."""

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            login(request, form.get_user())
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Unable to log in.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    """View function for user logout."""
    if request.user.is_authenticated:
        messages.error(request, "Logout failed, please try again")
    else: 
        messages.success(request, "Logout successful, see you soon!")
    return render(request, 'home.html')

# Create your views here.
