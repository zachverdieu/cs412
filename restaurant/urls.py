# File: restaurant/urls.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/16/2025
# Description: File containing url-to-view mapping for restaurant application

from django.urls import path
from django.conf import settings
from . import views

# URL patterns to specific url app
urlpatterns = [ 
    path(r'', views.main, name="restaurant"),
    path(r'order', views.order, name="order"),
    path(r'confirmation', views.confirmation, name="confirmation"),

]