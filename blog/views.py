from django.shortcuts import render
from .models import Article
from django.views.generic import ListView       #a way to send and render data 

class ShowAllView(ListView):
    # class definition, not a function
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

