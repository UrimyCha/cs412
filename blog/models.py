#blog/models/py
# note: you do not have to make migrations if you are editing anything other than the model
# make migrations only if you make changes to the fields (will be a quiz question)

from django.db import models
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    """"Encapsulate the data for a blog Article by some author"""

    #data attributes
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    #image_url = models.URLField(blank=True) #new field == leave it as blank for existing fields that do not have this field
    image_file = models.ImageField(blank=True)

    def __str__(self):
        """Return a string representation of the Article"""
        return f'{self.title} by {self.author}'
    
    def get_comments(self):
        '''Retrieve all comments for this article'''

        # use the ORM to filter comments where this instance of Article is the FK
        comments = Comment.objects.filter(article=self)     # could have used pk of this object or just self
        return comments
    
    def get_absolute_url(self):
        '''Return the URL to display this Article.'''
        return reverse('article', kwargs={'pk':self.pk})

class Comment(models.Model):
    '''ecapsulate a comment on an article'''
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of this object"""
        return f'{self.text}'


