from django.db import models

# Create your models here.
class Profile(models.Model):
    #first name, last name, city, email address, and a profile image url.
    firstname = models.TextField(blank=False)
    lastname = models.Textfield(blank=False)
    city = models.Textfield(blank=False)
    email = models.Textfield(blank=False)
    lastname = models.Textfield(blank=False)
    image_url = models.URLField(blank=False)

    






