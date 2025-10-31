# File: voter_analytics/views.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 10/31/2025
# Description: Views file which handles requests to voter_analytics app

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from . models import Voter
from datetime import date
import urllib.parse

import plotly
import plotly.graph_objs as go

class VoterListView(ListView):
    '''view to display voters'''

    model = Voter
    template_name = "voter_analytics/voters.html"
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        ''' filters the records, returning those that satisfy the query'''

        voters = super().get_queryset()

        # filter based on party affiliation
        party = self.request.GET.get('party_affiliation')
        if party:
            voters = voters.filter(party_affiliation__iexact=party)
            print(self.request.GET)

        # filter based on minimum birth year
        min_birth_year = self.request.GET.get('min_birth_year')
        if min_birth_year:
            min_birth_date = date(int(min_birth_year), 1, 1)
            voters = voters.filter(date_of_birth__gte=min_birth_date)

        # filter based on maximum birth year
        max_birth_year = self.request.GET.get('max_birth_year')
        if max_birth_year:
            max_birth_date = date(int(max_birth_year), 12, 31)
            voters = voters.filter(date_of_birth__lte=max_birth_date)

        # filter based on voter score
        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            voters = voters.filter(voter_score=voter_score)

        # filter based on whether they voted in past elections
        for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
            if self.request.GET.get(field):
                voters = voters.filter(**{field: 'TRUE'})

        return voters

    def get_context_data(self, **kwargs):
        '''provides context veriables for use in template'''

        context = super().get_context_data(**kwargs)
        current_year = date.today().year
        context['all_years'] = list(range(current_year, 1919, -1))
        context['scores'] = range(0, 6)
        context['party_affiliation'] = self.request.GET.get('party_affiliation')
        context['min_birth_year'] = self.request.GET.get('min_birth_year')
        context['max_birth_year'] = self.request.GET.get('max_birth_year')
        context['voter_score'] = self.request.GET.get('voter_score')
        context['v20state'] = self.request.GET.get('v20state')
        context['v21town'] = self.request.GET.get('v21town')
        context['v21primary'] = self.request.GET.get('v21primary')
        context['v22general'] = self.request.GET.get('v22general')
        context['v23town'] = self.request.GET.get('v23town')
        context['action'] = 'voters_list'

        return context

class VoterDetailView(DetailView):
    '''view to display a single voter'''

    model = Voter
    template_name = "voter_analytics/voter.html"
    context_object_name = "voter"

    def get_context_data(self, **kwargs):
        '''provides context veriables for use in template'''

        context = super().get_context_data(**kwargs)
        voter = context['voter']
        address = f"{voter.street_number} {voter.street_name}, Boston, MA {voter.zip_code}"
        google_maps = f"https://www.google.com/maps/search/{address.replace(' ', '+')}"
        context['maps'] = google_maps

        return context

class VoterGraphsView(ListView):
    '''view for graphs representing voting data'''

    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voter'

    def get_queryset(self):
        ''' filters the records, returning those that satisfy the query'''

        voters = Voter.objects.all()

        # party affiliation
        party_affiliation = self.request.GET.get('party_affiliation')
        if party_affiliation:
            voters = voters.filter(party_affiliation__iexact=party_affiliation)
            print(self.request.GET)

        # minimum birth year
        min_birth_year = self.request.GET.get('min_birth_year')
        if min_birth_year:
            min_birth_date = date(int(min_birth_year), 1, 1)
            voters = voters.filter(date_of_birth__gte=min_birth_date)

        # maximum birth year
        max_birth_year = self.request.GET.get('max_birth_year')
        if max_birth_year:
            max_birth_date = date(int(max_birth_year), 12, 31)
            voters = voters.filter(date_of_birth__lte=max_birth_date)

        # voter score
        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            voters = voters.filter(voter_score=voter_score)

        # voted elections
        for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
            if self.request.GET.get(field):
                voters = voters.filter(**{field: 'TRUE'})

        return voters

    def get_context_data(self, **kwargs):
        """
        provides context to template
        """

        context = super().get_context_data(**kwargs)
        filtered = self.get_queryset()

        # bar graph 1
        birthyear = [voter.date_of_birth.year for voter in filtered]
        fig_one = go.Histogram(x=birthyear, nbinsx=100)
        title_one = f"Voter Distribution by Birth Year (n={len(birthyear)})"

        layout1 = go.Layout(
            bargap=0.5,
            xaxis=dict(title='Birth Year'),
            yaxis=dict(title='Count')
        )

        bar1 = plotly.offline.plot({"data": [fig_one],
                                               "layout": layout1,
                                               "layout_title_text": title_one,},
                                              auto_open=False,
                                              output_type="div")

        # pie chart
        party_count = {}
        for voter in filtered:
            party = voter.party_affiliation
            party_count[party] = party_count.get(party, 0) + 1
        fig_two = go.Pie(labels=list(party_count.keys()), values=list(party_count.values()))
        title_two = f"Voter Distribution by Party (n={len(filtered)})"
        pie = plotly.offline.plot({"data": [fig_two],
                                               "layout_title_text": title_two,},
                                                auto_open=False,
                                                output_type="div")

        # bar graph 2
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        vote_count = []
        for election in elections:
            count = filtered.filter(**{election: 'TRUE'}).count()
            vote_count.append(count)
        fig_three = go.Bar(x=elections, y=vote_count)
        title_three = f"Vote Count by Voted Elections (n={Voter.objects.count()})"
        bar2 = plotly.offline.plot({"data": [fig_three],
                                                   "layout_title_text": title_three,},
                                                    auto_open=False,
                                                    output_type="div")

        # graphs
        context['graph_birth'] = bar1
        context['graph_party'] = pie
        context['graph_elections'] = bar2

        current_year = date.today().year
        context['all_years'] = list(range(current_year, 1919, -1))
        context['scores'] = range(0, 6)

        context['party_affiliation'] = self.request.GET.get('party_affiliation')
        context['min_birth_year'] = self.request.GET.get('min_birth_year')
        context['max_birth_year'] = self.request.GET.get('max_birth_year')
        context['voter_score'] = self.request.GET.get('voter_score')
        context['action'] = 'graphs'

        return context