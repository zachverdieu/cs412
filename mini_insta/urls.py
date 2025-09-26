# File: mini_insta/urls.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/25/2025
# Description: File containing url-to-view mapping for mini_insta application

from django.urls import path
from .views import ProfileListView, ProfileDetailView

urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
]