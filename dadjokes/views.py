from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Joke, Picture
import random
from rest_framework import generics
from .serializers import *

# Create your views here.

class RandomJokeView(DetailView):
    '''Display single randomly selected joke'''

    model = Joke
    template_name = "dadjokes/random.html"
    context_object_name = "joke"

    # methods
    def get_object(self):
        '''return one instance of Article object at random'''

        all_jokes = Joke.objects.all()
        joke = random.choice(all_jokes)
        return joke

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find and add random picture to the context data
        all_pictures = Picture.objects.all()
        picture = random.choice(all_pictures)

        # add this picture into the context dictionary
        context['picture'] = picture
        return context

class JokeListView(ListView):
    '''Display all Jokes'''

    model = Joke
    template_name = "dadjokes/jokes.html"
    context_object_name = "jokes"

class JokeDetailView(DetailView):
    '''Display a single joke object'''

    model = Joke
    template_name = "dadjokes/joke.html"
    context_object_name = "jokes"

class PictureListView(ListView):
    '''Display all Pictures'''

    model = Picture
    template_name = "dadjokes/pictures.html"
    context_object_name = "pictures"

class PictureDetailView(DetailView):
    '''Display a single picture object'''

    model = Picture
    template_name = "dadjokes/picture.html"
    context_object_name = "picture"

class RandomJokeAPIView(generics.RetrieveAPIView):
    ''' API view to return a random joke'''

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

    def get_object(self):
        ''' Fetch Joke object for view to return '''

        # Fetch all jokes
        jokes = self.get_queryset()
        # Return a random joke
        return random.choice(jokes)

class JokeListAPIView(generics.ListCreateAPIView):
    ''' API view to return a listing of joke objects and create one'''

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    ''' API view to return a single joke by primary key'''

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class RandomPictureAPIView(generics.RetrieveUpdateDestroyAPIView):
    ''' API view to return a random picture'''

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

    def get_object(self):
        ''' Fetch Picture object for view to return '''
        
        # Fetch all jokes
        picture = self.get_queryset()
        # Return a random joke
        return random.choice(picture)

class PictureListAPIView(generics.ListCreateAPIView):
    ''' API view to return a listing of picture objects and create one'''

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    ''' API view to return a single picture by primary key'''

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

