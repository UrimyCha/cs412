from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    # first name, last name, city, email address, and a profile image url.
    firstname = models.TextField(blank=False)
    lastname = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=False)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'
    
    def get_status_messages(self):
        '''Retrieve all comments for this article'''

        # use the ORM to filter comments where this instance of Article is the FK
        message = StatusMessage.objects.filter(profile=self)     # could have used pk of this object or just self
        return message
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})

class StatusMessage(models.Model):
    # model the data attributes of Facebook status message
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of this object"""
        return f'{self.message}'
    
    def get_images(self):
        """ Return all images associated with this status message """
        image = Image.objects.filter(status_message=self)    
        return image

class Image(models.Model):
    # model for uploading image files to a status message
    timestamp = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True)
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.image}'







