# File: quotes/views.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/11/2025
# Description: File containing views functions for quote application

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random, time

# List of pictures

pictures = [
    "https://yt3.googleusercontent.com/Nk08bfKqYHzaOG4nmgFTQLHCyMgdNLjuLPeT1tAvXYKj6C6U_yzRD9kTcgWayyg2pNFHMnvY-Q=s900-c-k-c0x00ffffff-no-rj",
    "https://assets.vogue.com/photos/59839f025ce7e830e273e428/master/w_2560%2Cc_limit/00-lede-barack-obama-five-things.jpg",
    "https://www.brookings.edu/wp-content/uploads/2017/05/barack_obama001.jpg?quality=75",
]

# List of quotes
quotes = [
    "Change will not come if we wait for some other person, or if we wait for some other time. We are the ones we've been waiting for. We are the change that we seek.",
    "In the face of impossible odds, people who love this country can change it.",
    "Why can't I just eat my waffle?"
]

# Create your views here.

def quote(request):
    '''Function to respond to "quote" request.'''

    template_name = 'quotes/quote.html'

    context = {
        "quote": random.choice(quotes),
        "picture": random.choice(pictures),
        "time": time.ctime(),
    }

    return render(request, template_name, context)

def show_all(request):
    '''Function to respond to "show_all" request.'''

    template_name = 'quotes/show_all.html'

    context = {
        "quotes": quotes,       
        "pictures": pictures,  
        "time": time.ctime(),
    }

    return render(request, template_name, context)

def about(request):
    '''Function to respond to "about" request.'''

    template_name = 'quotes/about.html'

    context = {
        "time": time.ctime(),
    }

    return render(request, template_name, context)
