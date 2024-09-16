from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms
from django.forms import TextInput
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        fields = ('username', 'password1', 'password2')
        model = User
    
    username = UsernameField(
        label='Username:',
        widget=TextInput(attrs={'class': 'form-input'}),
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        )
    password1 = forms.CharField(
        label='Password:',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        help_text=mark_safe("""
Your password:<br>
* Can't be too similar to your other personal information.<br>
* Must contain at least 8 characters.<br>
* Can't be a commonly used password.<br>
* Can't be entirely numeric.
                            """)
        )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        help_text="Enter the same password as before, for verification."
        )