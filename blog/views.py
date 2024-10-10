from django.shortcuts import render
from .models import Article
from .forms import CreateCommentForm
from django.views.generic import ListView, DetailView, CreateView       #a way to send and render data 
import random
from django.urls import reverse
from typing import Any

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

class CreateCommentView(CreateView):
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
