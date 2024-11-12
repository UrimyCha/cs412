from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Result
import plotly
import plotly.graph_objects as go

# Create your views here.

class ResultListView(ListView):
    """ View to list the results of the marathon """

    template_name = "marathon_analytics/results.html"
    model = Result
    context_object_name = "results"
    paginate_by = 50

    def get_queryset(self) -> QuerySet[Any]:
        """Return subset of records"""

        qs = super().get_queryset()

        if 'city' in self.request.GET:
            city = self.request.GET['city']
            qs = Result.objects.filter(city=city)

        return qs
    
class ResultDetailView(DetailView):
    '''Show the results for one record'''

    template_name = 'marathon_analytics/result_detail.html'
    model = Result
    context_object_name = 'r'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''
        add some data to the context object, including graphs
        '''
        context = super().get_context_data(**kwargs)
        r = context['r'] # our result

        x = [f'Runners who passed by {r.first_name}',
             f'Runnner who Passed {r.first_name}']
        
        y = [r.get_runners_passed(),
             r.get_runners_passed_by()]
        
        # print(f'x={x}')
        # print(f'y={y}')

        fig = go.Bar(x=x, y=y)
        title_text = f"Runners Passed/Passed By"
        graph_div_passed = plotly.offline.plot({"data": [fig],}, 
                                         auto_open=False, 
                                         output_type="div",
                                         ) 
        context['graph_div_passed'] = graph_div_passed

        # build a pie chart of first half/ second half
        x = ['first half', 'second half']
        first_half_seconds = (r.time_half1.hour * 60 + r.time_half1.minute) * 60 + r.time_half1.second
        second_half_seconds = (r.time_half2.hour * 60 + r.time_half2.minute) * 60 + r.time_half2.second
        y = [first_half_seconds , second_half_seconds]

        # print(f'x={x}')
        # print(f'y={y}')

        fig = go.Pie(labels=x, values=y)
        pie_div = plotly.offline.plot({"data":[fig],},
                                      auto_open=False,
                                      output_type="div",
                                      )
        context['pie_div'] = pie_div

        return context