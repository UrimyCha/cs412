from django.shortcuts import render

# Create your views here.
from .models import Profile
from django.views.generic import ListView       #a way to send and render data 

class ShowAllProfilesView(ListView):
    # class definition, not a function
    model = Profile
    template_name = 'minifb/show_all_profiles.html'
    context_object_name = 'profiles'