from django.shortcuts import render
from django.views.generic import ListView
from .models import Voter

# Create your views here.
class VoterListView(ListView):
    template_name = "voter_analytics/voters.html"
    model = Voter
    context_object_name = "voters"