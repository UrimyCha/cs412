from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['firstname', 'lastname', 'email', 'city', 'image_url']

    firstname = forms.CharField(label="First Name", required=True)
    lastname = forms.CharField(label="Last Name", required=True)
    email = forms.CharField(label="Email", required=True)
    city = forms.CharField(label="City", required=True)

class CreateStatusMessageForm(forms.ModelForm):
    
    class Meta:
        model = StatusMessage
        fields = ['message',]