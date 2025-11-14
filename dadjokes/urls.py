# File: dadjokes/urls.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 11/12/2025
# Description: File containing url-to-view mapping for dadjokes application

from django.urls import path
from .views import *

urlpatterns = [
    path('', RandomJokeView.as_view(), name="home"),
    path('random', RandomJokeView.as_view(), name="random"),
    path('jokes', JokeListView.as_view(), name="jokes"),
    path('joke/<int:pk>', JokeDetailView.as_view(), name="joke"),
    path('pictures', PictureListView.as_view(), name="pictures"),
    path('picture/<int:pk>', PictureDetailView.as_view(), name="picture"),
    # API Views:
    path('api/', RandomJokeAPIView.as_view(), name='home_joke_api'),
    path('api/random', RandomJokeAPIView.as_view(), name='random_joke_api'),
    path('api/jokes', JokeListAPIView.as_view(), name='random_joke_api'),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view(), name='random_joke_api'),
    path('api/pictures', PictureListAPIView.as_view(), name='random_joke_api'),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view(), name='random_joke_api'),
    path('api/random_picture', RandomPictureAPIView.as_view(), name='random_picture_api'),

]