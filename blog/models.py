#blog/models/py
# note: you do not have to make migrations if you are editing anything other than the model
# make migrations only if you make changes to the fields (will be a quiz question)

from django.db import models

# Create your models here.
class Article(models.Model):
    """"Encapsulate the data for a blog Article by some author"""

    #data attributes
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True) #new field == leave it as blank for existing fields that do not have this field

    def __str__(self):
        """"Return a string representation of the Article"""
        return f'{self.title} by {self.author}'



