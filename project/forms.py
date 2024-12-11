from django import forms
from .models import *
    
class CreateReservationForm(forms.Form):
    ''' Combines Customer ModelForm and Reservation ModelForm into one so that 
        all of the necessary information is collected at once
    '''
    TIME_CHOICES = (('10:00:00', '10 AM'),
                    ('10:30:00', '10:30 AM'),
                    ('11:00:00', '11 AM'),
                    ('11:30:00', '11:30 AM'),
                    ('12:00:00', 'Noon'),
                    ('12:30:00', '12:30 PM'),
                    ('13:00:00', '1 PM'),
                    ('13:30:00', '1:30 PM'),
                    ('14:00:00', '2 PM'), 
                    ('14:30:00', '2:30 PM'), 
                    ('15:00:00', '3 PM'),
                    ('15:30:00', '3:30 PM'),
                    ('16:00:00', '4 PM'),
                    ('16:30:00', '4:30 PM'),
                    ('17:00:00', '5 PM'),
                    ('17:30:00', '5:30 PM'),
                    ('18:00:00', '6 PM'),
                    ('18:30:00', '6:30 PM'),
                    ('19:00:00', '7 PM'),
                    ('19:30:00', '7:30 PM'),
                    ('20:00:00', '8 PM'),)

    # Fields from Cutomer model
    first_name = forms.CharField(max_length=100, required=True, label="First Name")
    last_name = forms.CharField(max_length=100, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    phone_number = forms.CharField(max_length=10, required=True, label="Phone Number")

    # Fields from Reservation model
    reservation_date = forms.DateField(required=True,
                                       widget=forms.DateInput(format="%Y-%m-%d", 
                                                              attrs={"type": "date"}),
                                        input_formats=["%Y-%m-%d"],
                                        label="Reserve Date")
    reservation_time = forms.ChoiceField(choices=TIME_CHOICES, required=True, label="Select Reservation Time Block")
    party_size = forms.IntegerField(min_value=1, max_value=8, required=True,
                                    widget=forms.NumberInput(attrs={'placeholder': 'Party Size (1-8)'},),
                                    label="Party Size"
                                    )
    
class AdoptionForm(forms.Form):
    ''' 
        Includes Customer and Cat model fields in the Adoption form to collect all necessary
        information to apply for an adoption
    '''
    # Fields from Customer model
    first_name = forms.CharField(max_length=100, required=True, label="First Name")
    last_name = forms.CharField(max_length=100, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    phone_number = forms.CharField(max_length=10, required=True, label="Phone Number")

    # Field from Cat model --> just to identify which cat for this adoption
    name = forms.CharField(max_length=100, required=True, label="Which cat are you interested in?")

    # Fields from Adoption model
    address = forms.CharField(max_length=200, required=True, label="Home Address")
    other_pets_num = forms.IntegerField(required=True, label="How many other pets do you have?")
    children_num = forms.IntegerField(required=True, label="How many children live with you?")
    household_size = forms.IntegerField(required=True, label="Household Size (including yourself)")

class ReservationLookupForm(forms.Form):
    email = forms.EmailField(label="Enter your email to find reservations")

class UpdateReservationForm(forms.ModelForm):
    '''A form to update a message to the database.'''
    class Meta:
        model = Reservation
        fields = ['reservation_date', 'reservation_time', 'party_size']  # which fields from model should we use