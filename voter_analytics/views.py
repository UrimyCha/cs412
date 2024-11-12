from django.shortcuts import render
from django.views.generic import *
from .models import Voter
from django.db.models.query import QuerySet
from typing import Any
import plotly
import plotly.graph_objects as go


# Create your views here.
class VoterListView(ListView):
    template_name = "voter_analytics/voters.html"
    model = Voter
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = Voter.objects.all()

        if 'party' in self.request.GET:
            party = self.request.GET['party']
            qs = qs.filter(party=party)
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            qs = qs.filter(voter_score=voter_score)
        if 'min_dob_year' in self.request.GET:
            min_dob_year = self.request.GET['min_dob_year']
            min_dob_year += "-01-01"
            qs = qs.filter(dob__gte=min_dob_year)
        if 'max_dob_year' in self.request.GET:
            max_dob_year = self.request.GET['max_dob_year']
            max_dob_year += "-01-01"
            qs = qs.filter(dob__lt=max_dob_year)
        if 'v20state' in self.request.GET:
            qs = qs.filter(v20state='TRUE')
        if 'v21town' in self.request.GET:
            qs = qs.filter(v21town='TRUE')
        if 'v21primary' in self.request.GET:
            qs = qs.filter(v21primary='TRUE')
        if 'v22general' in self.request.GET:
            qs = qs.filter(v22general='TRUE')
        if 'v23town' in self.request.GET:
            qs = qs.filter(v23town='TRUE')

        return qs

class VoterDetailView(DetailView):
    template_name = "voter_analytics/voter_detail.html"
    model = Voter
    context_object_name = "voter"

class GraphView(ListView):
    template_name = "voter_analytics/graphs.html"
    model = Voter
    context_object_name = "v"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        voters = self.get_queryset()

        # Bar chart for voter DOB distribution
        dob_count = {}

        for v in voters:
            year = v.dob.year
            dob_count[year] = dob_count.get(year,0) + 1

        x = list(dob_count.keys())
        y = list(dob_count.values())

        fig = go.Bar(x=x, y=y)
        title_text = f"Voter Distribution by Year of Birth"
        graph_dob_counts = plotly.offline.plot({"data": [fig],
                                                "layout_title_text": title_text}, 
                                         auto_open=False, 
                                         output_type="div",
                                         ) 
        context['graph_dob_counts'] = graph_dob_counts


        # Pie chart for voter party affiliations
        party_counts = {}
        for v in voters:
            party_counts[v.party] = party_counts.get(v.party, 0) + 1
        
        x = list(party_counts.keys())
        y = list(party_counts.values())

        fig = go.Pie(labels=x, values=y)
        title_text = f"Voter Distribution by Party Affiliation"

        pie_div = plotly.offline.plot({"data":[fig],
                                       "layout_title_text": title_text},
                                      auto_open=False,
                                      output_type="div",
                                      )
        context['pie_div'] = pie_div

        # Bar chart for election participation
        elections = {
            "v20state" : 0,
            "v21town" : 0,
            "v21primary" : 0,
            "v22general" : 0,
            "v23town" : 0
        }

        for v in voters:
            if v.v20state == "TRUE":
                elections["v20state"] += 1
            if v.v21town == "TRUE":
                elections["v21town"] += 1
            if v.v21primary == "TRUE":
                elections["v21primary"] += 1
            if v.v22general == "TRUE":
                elections["v22general"] += 1
            if v.v23town == "TRUE":
                elections["v23town"] += 1

        x = list(elections.keys())
        y = list(elections.values())

        fig = go.Bar(x=x, y=y)
        title_text = f"Voter Distribution by Election"
        graph_elections = plotly.offline.plot({"data": [fig],
                                                "layout_title_text": title_text}, 
                                         auto_open=False, 
                                         output_type="div",
                                         ) 
        context['graph_elections'] = graph_elections

        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = Voter.objects.all()

        if 'party' in self.request.GET:
            party = self.request.GET['party']
            qs = qs.filter(party=party)
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            qs = qs.filter(voter_score=voter_score)
        if 'min_dob_year' in self.request.GET:
            min_dob_year = self.request.GET['min_dob_year']
            min_dob_year += "-01-01"
            qs = qs.filter(dob__gte=min_dob_year)
        if 'max_dob_year' in self.request.GET:
            max_dob_year = self.request.GET['max_dob_year']
            max_dob_year += "-01-01"
            qs = qs.filter(dob__lt=max_dob_year)
        if 'v20state' in self.request.GET:
            qs = qs.filter(v20state='TRUE')
        if 'v21town' in self.request.GET:
            qs = qs.filter(v21town='TRUE')
        if 'v21primary' in self.request.GET:
            qs = qs.filter(v21primary='TRUE')
        if 'v22general' in self.request.GET:
            qs = qs.filter(v22general='TRUE')
        if 'v23town' in self.request.GET:
            qs = qs.filter(v23town='TRUE')

        return qs
    
