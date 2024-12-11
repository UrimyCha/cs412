from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Customer(models.Model):
    """
    Model for collecting the contact information for each customer 
    that wants to make a reservation or adopt a cat

    note: phone_number field is from installed package "django-phonenumber-field"
    """
    first_name = models.CharField(blank=False, max_length=100)
    last_name = models.CharField(blank=False, max_length=100)
    email = models.EmailField(blank=False)
    phone_number = models.CharField(blank=False, max_length=11)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_reservations(self):
        ''' Retrieve all reservations this customer has ever made '''
        # use the ORM to filter reservations where this instance of Customer is the FK
        reservation = Reservation.objects.filter(customer=self)    
        return reservation
    
    def get_adoptions(self):
        ''' Retreive all of the adoption forms this customer has ever applied for '''
        adoption = Adoption.objects.filter(customer=self)
        return adoption
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})

class Cat(models.Model):
    """
    Model for storing information about each cat at the cafe and creating a profile
    name: cat name
    age: optional field in case the age is unknown
    personality_traits: optional field, would contain personality traits about the cat 
                        (e.g. "shy", "playful", "cuddly")
    image: profile picture for a cat
    adoptable: boolean field, true if adoptable and false if cat has been adopted or is a permanent resident
    """
    name = models.CharField(blank=False, max_length=100)
    age = models.IntegerField(blank=True)
    personality_traits = models.TextField(blank=True)
    adoptable = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return f'{self.name}, {self.age}'
    
    def get_images(self):
        """ Return all images associated with this cat """
        image = Image.objects.filter(cat=self)    
        return image
    
    def get_profile_img(self):
        """ Return the first image associated with this cat for its profile image"""
        image = Image.objects.filter(cat=self).first()    
        return image
    
class Image(models.Model):
    # model for uploading image files to a status message
    timestamp = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True)
    cat = models.ForeignKey("Cat", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.image}'

class Reservation(models.Model):
    """
    Model for customers to make a reservation to come to the cafe and interact with the cats
    customer: foreign key to Customer model
    reservation_date: date that the customer would like to come to the cafe
    reservation_time: specific time that the customer would like to reserve
    party_size: how many people the reservation is for, min is 1 person 
                (for the person making the reservation) and max party size is 8.
    status: status between "scheduled", "cancelled", or "pending"
    """
    STATUS_CHOICES = {
        "SCHEDULED" : "scheduled",
        "COMPLETED" : "completed"
    }

    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    reservation_date = models.DateField(blank=False, default=datetime.now)
    reservation_time = models.TimeField(blank=False)
    party_size = models.IntegerField(
        default=1,
        blank=False,
        validators=[
            MaxValueValidator(8),
            MinValueValidator(1)
        ]
     )
    status = models.CharField(max_length=10,choices=STATUS_CHOICES, default="SCHEDULED")

    def __str__(self):
        return f'{self.customer} at {self.reservation_date}'

class Adoption(models.Model):
    """
    Model for the when a customer wants to adopt a cat
    customer: foreign key to Customer model
    cat: foreign key to Cat model
    application_date: instance of this model will be created when a customer submits a application form,
                        so field is a DateTimeField set to automatically when it was created
    adoption_date: optional field, blank if the adoption has not gone through yet, but will be set if it has
    address: customer address
    other_pet_num: field to ask how many other pets a customer already has
    children_num: field to ask how many children a customer has
    household_size: field to ask how many people live in the customers home (including themself)
    status: current status of the adoption process (e.g. "approved", "rejected", "pending")
    notes: optional field, any notes that the person reviewing the application may have on it
    """
    ADOPTION_STATUS = {
        "APPROVED" : "approved",
        "REJECTED" : "rejected",
        "PENDING" : "pending"
    }

    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    cat = models.ForeignKey("Cat", on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now=True)
    adoption_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=200,blank=False, null=True)
    other_pets_num = models.IntegerField(blank=True, null=True, default=0)
    children_num = models.IntegerField(blank=True, null=True, default=0)
    household_size = models.IntegerField(blank=False, null=True, default=1)
    status = models.CharField(max_length=8,
                              blank=False, 
                              choices=ADOPTION_STATUS,
                              default="PENDING")
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.customer} - {self.cat}'

