from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Profile, Image, StatusMessage
from django.views.generic import *      #a way to send and render data 
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.urls import reverse
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin 

class ShowAllProfilesView(ListView):
    # class definition, not a function
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

    def dispatch(self, *args, **kwargs):
        print(f"self.request.user={self.request.user}")
        return super().dispatch(*args, **kwargs)

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        #get the super class version of the context data
        context = super().get_context_data(**kwargs)

        #add the article to the context data
        context['profile_user'] = self.get_object().user
        return context

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

class CreateStatusMessageView(LoginRequiredMixin,CreateView):
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
        
        # save the status message to database
        sm = form.save()

        # read the file from the form:
        files = self.request.FILES.getlist('files')

        for file in files:
            # Create a new Image object for each file
            image = Image(status_message=sm, image=file)
            image.save()  # Save each image object to the database

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
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

class UpdateProfileView(LoginRequiredMixin,UpdateView):
    '''A view to update an Article and save it to the database.'''
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    model = Profile
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''A view to delete a comment and remove it from the database.'''
    template_name = "mini_fb/delete_status_form.html"
    model = StatusMessage
    context_object_name = 'message'

    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
        # get the pk for this comment
        pk = self.kwargs.get('pk')
        message = StatusMessage.objects.filter(pk=pk).first() # get one object from QuerySet
        
        # find the article to which this Comment is related by FK
        profile = message.profile
        
        # reverse to show the article page
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

class UpdateStatusMessageView(LoginRequiredMixin,UpdateView):
    '''A view to update an Article and save it to the database.'''
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"
    model = StatusMessage
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
        # get the pk for this comment
        pk = self.kwargs.get('pk')
        message = StatusMessage.objects.filter(pk=pk).first() # get one object from QuerySet
        
        # find the article to which this Comment is related by FK
        profile = message.profile
        
        # reverse to show the article page
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        # Retrieve the Profile instance for the user initiating the friendship
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        # Retrieve the Profile instance for the friend to be added
        other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])
        
        # Call the add_friend method to add the friendship, if it doesn't already exist
        profile.add_friend(other_profile)
        
        # Redirect back to the profile page (or any other desired page)
        return redirect('show_profile', pk=profile.pk)
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
class ShowFriendSuggestionsView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get friend suggestions by calling the method on the profile instance
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
class ShowNewsFeedView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get friend suggestions by calling the method on the profile instance
        context['news_feed'] = self.object.get_news_feed()
        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 