# File: mini_insta/urls.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 10/31/2025
# Description: File containing url-to-view mapping for voter_analytics application

from django.urls import path
from . import views 
from .views import *

urlpatterns = [
	path(r'', views.VoterListView.as_view(), name='voters'),
    path(r'voters_list', views.VoterListView.as_view(), name='voters_list'),
    path(r'voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter'),
    path(r'graphs/', views.VoterGraphsView.as_view(), name='graphs'),
]