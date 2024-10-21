from django import forms
from .models import Comment, Article

class CreateCommentForm(forms.ModelForm):
    '''A form to create Comment data'''

    class Meta:
        ''' associate this form with the Comment model'''
        model = Comment
        #fields = ['article', 'author', 'text', ] 
        # took out article
        fields = ['author', 'text', ] 

class CreateArticleForm(forms.ModelForm):
    ''' form to create a new Article'''
    
    class Meta:
        model = Article
        fields = ['author', 'title', 'text', 'image_file']


