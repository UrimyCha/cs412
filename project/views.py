from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic import *  
from typing import Any
from django.urls import reverse, reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.db.models.query import QuerySet


def menu(request):
    ''' Rendering the static menu page '''
    return render(request, 'project/menu.html')

def homepage(request):
    ''' Rendering the static menu page '''
    return render(request, 'project/homepage.html')

def form_view(request: HttpRequest) -> HttpResponse:
    ''' 
        View to render a calendar date selector for reservation date input
        Borrowed from: https://pythonassets.com/posts/date-field-with-calendar-widget-in-django-forms/
    '''
    if request.method == "POST":
        form = CreateReservationForm(request.POST)
        if form.is_valid():
            # Receive the submitted date as an instance of `datetime.date`.
            date: datetime.date = form.cleaned_data["reservation_date"]
            # Do something with that value, such as storing it in a database
            # or displaying it to the user.
            date_output = date.strftime("%d %b %Y")
            return HttpResponse(f"The submitted date is: {date_output}")
    else:
        form = CreateReservationForm()
    ctx = {"form": form}
    return render(request, "project/create_reservation.html", ctx)


class ShowAllCatsView(ListView):
    model = Cat
    template_name = 'project/show_all_cats.html'
    context_object_name = 'cats'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = Cat.objects.all()

        if 'min_age' in self.request.GET:
            min_age = self.request.GET['min_age']
            qs = qs.filter(age__gte=min_age)
        if 'max_age' in self.request.GET:
            max_age = self.request.GET['max_age']
            qs = qs.filter(age__lte=max_age)
        if 'shy' in self.request.GET:
            qs = qs.filter(personality_traits__contains='shy') 
        if 'cuddly' in self.request.GET:
            qs = qs.filter(personality_traits__contains='cuddly')     
        if 'playful' in self.request.GET:
            qs = qs.filter(personality_traits__contains='playful') 
        if 'goofy' in self.request.GET:
            qs = qs.filter(personality_traits__contains='goofy')   
        if 'sweet' in self.request.GET:
            qs = qs.filter(personality_traits__contains='sweet')  
        if 'chill' in self.request.GET:
            qs = qs.filter(personality_traits__contains='chill')  
        if 'talkative' in self.request.GET:
            qs = qs.filter(personality_traits__contains='talkative')  
        if 'adoptable' in self.request.GET:
            adoption = self.request.GET['adoptable']
            qs = qs.filter(adoptable=adoption)

        return qs
    

class ShowCatProfile(DetailView):
    model = Cat
    template_name = 'project/show_cat_profile.html'
    context_object_name = 'cat'


class CreateReservationView(FormView):
    form_class = CreateReservationForm
    template_name = 'project/create_reservation.html'

    def form_valid(self, form):
        ''' logic for processing form data '''
        # Getting customer fields 
        c_fname = form.cleaned_data['first_name']
        c_lname = form.cleaned_data['last_name']
        c_email = form.cleaned_data['email']

        customers = Customer.objects.all()

        # check if this customer has been here before, if not then create new customer instance
        if customers.filter(first_name=c_fname, last_name=c_lname, email=c_email).exists() == False:
            customer = Customer.objects.create(
                first_name=c_fname,
                last_name=c_lname,
                email=c_email,
                phone_number=form.cleaned_data['phone_number'],
            )
        # Create Reservation
        self.reservation = Reservation.objects.create(
            customer=customer,
            reservation_date=form.cleaned_data['reservation_date'],
            reservation_time=form.cleaned_data['reservation_time'],
            party_size=form.cleaned_data['party_size'],
        )

        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('reservation_confirm', kwargs={'pk':self.reservation.pk})
    

class ReservationConfirmView(TemplateView):
    ''' View for showing a confirmation page after successfully making a reservation'''
    template_name = 'project/reservation_confirm.html'

    def get_context_data(self, **kwargs):
        ''' Get all of the reservation details '''
        context = super().get_context_data(**kwargs)
        # Get the reservation pk from the URL
        pk = self.kwargs['pk']
        # Fetch the reservation details
        context['reservation'] = Reservation.objects.get(pk=self.kwargs['pk'])
        return context
    

class AdoptionFormView(FormView):
    '''
        Form view to render the Adoption Form and handle processing form inputs
    '''
    form_class = AdoptionForm
    template_name = 'project/adoption_form.html'

    def get_context_data(self, **kwargs: Any):
        # Adding user creation form to context data
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        # Getting customer fields 
        c_fname = form.cleaned_data['first_name']
        c_lname = form.cleaned_data['last_name']
        c_email = form.cleaned_data['email']

        customers = Customer.objects.all()

        # check if this customer has been here before --> if so, attach user instance to customer
        if (customers.filter(first_name=c_fname).exists() | 
            customers.filter(last_name=c_lname).exists() |
            customers.filter(email=c_email).exists()) == False:
            customer = Customer.objects.create(
                first_name=c_fname,
                last_name=c_lname,
                email=c_email,
                phone_number=form.cleaned_data['phone_number'],
            )
        else:
            customer = customers.filter(first_name=c_fname)
            customer = customers.filter(last_name=c_lname)
            customer = customers.filter(email=c_email).first()

        # find Cat object instance to attach new Adoption object to
        cat = Cat.objects.get(name=form.cleaned_data['name'])

        # Create Adoption object instance
        self.adoption = Adoption.objects.create(
            customer=customer,
            cat=cat,
            address=form.cleaned_data['address'],
            other_pets_num=form.cleaned_data['other_pets_num'],
            children_num=form.cleaned_data['children_num'],
            household_size=form.cleaned_data['household_size']
        )
        
        # Delegate the rest to the super class’ form_valid method.
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('adoption_confirm', kwargs={'pk':self.adoption.pk})
    

class AdoptionConfirmView(TemplateView):
    ''' View for showing a confirmation page after submitting an adoption application'''
    template_name = 'project/adoption_confirm.html'

    def get_context_data(self, **kwargs):
        ''' Get all of the reservation details '''
        context = super().get_context_data(**kwargs)
        # Get the adoption pk from the URL
        pk = self.kwargs['pk']
        # Fetch the adoption application details
        context['adoption'] = Adoption.objects.get(pk=self.kwargs['pk'])
        return context
    
class ReservationLookupView(FormView):
    template_name = 'project/reservation_lookup.html'
    form_class = ReservationLookupForm

    def form_valid(self, form):
        # Fetch the customer by email
        email = form.cleaned_data['email']
        try:
            customer = Customer.objects.get(email=email)
            reservations = Reservation.objects.filter(customer=customer)
            return self.render_to_response(self.get_context_data(reservations=reservations, customer=customer))
        except Customer.DoesNotExist:
            form.add_error('email', "No customer found with this email.")
            return self.form_invalid(form)

class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = UpdateReservationForm
    template_name = 'project/update_reservation.html'
    success_url = reverse_lazy('reservation_lookup')  # Redirect to the lookup page on success


class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'project/reservation_confirm_delete.html'
    success_url = reverse_lazy('reservation_lookup')  # Redirect to the lookup page on success

    