# File: quotes/urls.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/11/2025
# Description: File containing url-to-view mapping for quotes application

from django.urls import path
from django.conf import settings
from . import views

# URL patterns to specific url app
urlpatterns = [ 
    # path(r'', views.home, name="home"),
    path(r'', views.quote, name="quote"),
    path(r'show_all', views.show_all, name="show_all"),
    path(r'about', views.about, name="about"),

]