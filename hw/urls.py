# File: hw/urls.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/9/2025
# Description: 

from django.urls import path
from django.conf import settings
from . import views

# URL patterns to specific url app
urlpatterns = [ 
    #path(r'', views.home, name="home"),
    path(r'', views.home_page, name="home_page"),
    path(r'about', views.about, name="about"),

]