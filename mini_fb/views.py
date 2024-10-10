from django.shortcuts import render

# Create your views here.
from .models import Profile
from django.views.generic import ListView, DetailView, CreateView      #a way to send and render data 
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse
from typing import Any

class ShowAllProfilesView(ListView):
    # class definition, not a function
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_success_url(self) -> str:
        #return "blog/show_all"
        #return reverse("show_all")
        return reverse("show_profile", kwargs=self.kwargs)


    def form_valid(self, form):
        '''method executes after form submission'''
        print(f'CreateStatusMessageView.form_valid(): form={form.cleaned_data}')
        print(f'CreateStatusMessageView.form_valid(): self.kwargs={self.kwargs}')

        # find the article with the pk from the url
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        # attach the article to the comment
        # form.instance is the new Comment object
        form.instance.profile = profile

        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        #get the super class version of the context data
        context = super().get_context_data(**kwargs)

        # find the pk from the URL
        pk = self.kwargs['pk']

        # find the corresponding article
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        #add the article to the context data
        context['profile'] = profile
        return context

