from django.shortcuts import render
from .models import Article
from django.views.generic import ListView, DetailView       #a way to send and render data 
import random

class ShowAllView(ListView):
    # class definition, not a function
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

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


