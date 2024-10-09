from django.shortcuts import render

# Create your views here.
from .models import Profile
from django.views.generic import ListView, DetailView       #a way to send and render data 

class ShowAllProfilesView(ListView):
    # class definition, not a function
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'