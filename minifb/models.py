from django.db import models

# Create your models here.
class Profile(models.Model):
    #first name, last name, city, email address, and a profile image url.
    firstname = models.TextField(blank=False)
    lastname = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    lastname = models.TextField(blank=False)
    image_url = models.URLField(blank=False)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'








