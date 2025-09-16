# formdata/urls.py
# sverdieu@bu.edu 9/15/25
# Url patterns for formdata app

from django.urls import path
from django.conf import settings
from . import views

# URL Patterns for this app
urlpatterns = [
    path(r'', views.show_form, name="show_form"),
    path(r'submit', views.submit, name="submit"),
]