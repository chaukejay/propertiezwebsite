from django import forms
from .models import Agent

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = [
            'first_name', 'last_name', 'email', 'contact_number', 'ffc_id',
            'agency'
            ]