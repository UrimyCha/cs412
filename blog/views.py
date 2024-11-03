from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render, redirect

from .models import Article
from .forms import CreateCommentForm, CreateArticleForm
from django.views.generic import ListView, DetailView, CreateView       #a way to send and render data 
import random
from django.urls import reverse
from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm ## NEW


# NEW : want to be able to only show certain views if logged in, import a superclass
# multiple inheritance --> the order in which you put in the class matters
from django.contrib.auth.mixins import LoginRequiredMixin

class ShowAllView(ListView):
    # class definition, not a function
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

    def dispatch(self, *args, **kwargs):
        print(f"self.request.user={self.request.user}")
        return super().dispatch(*args, **kwargs)

class RandomArticleView(DetailView):
    '''Show one article selected at random'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get_object(self):
        # get all articles
        all_articles = Article.objects.all()
        #pick one at random
        return random.choice(all_articles)

class ArticleView(DetailView):
    '''Show one article by its primary key'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

class CreateCommentView(LoginRequiredMixin, CreateView):
    '''view to show/process the create comment form
    on GET: sends back the form
    on POST: read the form data, create an instance of Comment, save to database
    '''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self) -> str:
        #return "blog/show_all"
        #return reverse("show_all")
        return reverse("article", kwargs=self.kwargs)


    def form_valid(self, form):
        '''method executes after form submission'''
        print(f'CreateCommentView.form_valid(): form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid(): self.kwargs={self.kwargs}')

        # find the article with the pk from the url
        article = Article.objects.get(pk=self.kwargs['pk'])

        # attach the article to the comment
        # form.instance is the new Comment object
        form.instance.article = article

        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        #get the super class version of the context data
        context = super().get_context_data(**kwargs)

        # find the pk from the URL
        pk = self.kwargs['pk']

        # find the corresponding article
        article = Article.objects.get(pk=self.kwargs['pk'])

        #add the article to the context data
        context['article'] = article
        return context

class CreateArticleView(LoginRequiredMixin, CreateView):
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def get_login_url(self) -> str:
        ''' return the url required for login '''

        return reverse('login')

    def form_valid(self, form):
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')

        # Integrity error: need to associate a user to a new article
        # find which user is logged in
        user = self.request.user

        # attach the user to  the new article instance
        form.instance.user = user

        return super().form_valid(form)

class RegistrationView(CreateView):
    """Display and process the UserCreationForm for account registration"""

    template_name = 'blog/register.html'
    form_class = UserCreationForm

    def dispatch(self, *args, **kwargs):
        ''' handle the user creation process '''

        # handle the HTTP POST request
        if self.request.POST:
            print(f"self.request.POST = {self.request.POST}")
            # recontruct the UserCreationForm from the HTTP POST
            form = UserCreationForm(self.request.POST)

            # save the new User object (IMPORTANT FOR HW ASSIGNMENT!!!)
            user = form.save()     # creates a new user object instance in the database
            print(f"RegistrationView.form_valid(): Created user= {user}")   

            # log in the user
            login(self.request, user)
            print(f"RegistrationView.dispatch: user {user} is logged in")
            
            # redirect the user to some page view

            return redirect(reverse('show_all'))

        # let the superclass CreateView handle the HTTP GET
        return super().dispatch(*args, **kwargs)