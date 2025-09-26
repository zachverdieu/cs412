# File: mini_insta/urls.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/25/2025
# Description: views for mini_insta application
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.
class ProfileListView(ListView):
    '''Define a class to show all blog articles'''

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    '''Display a single profile'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"