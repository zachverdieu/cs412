# File: hw/views.py

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time, random

# Create your views here.
def home(request):
    '''Function to respond to "home" request.'''

    response_text = f'''
    <html>
    <h1>Hello, world</h1>
    <p>The current time is {time.ctime()}
    </html>
    '''

    return HttpResponse(response_text)

def home_page(request):
    '''Respond to URL '', delegate work to a tamplate.'''

    template_name = 'hw/home.html'
    # dict of context variables
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(65, 90)),
        "letter2": chr(random.randint(65, 90)),
        "number": random.randint(1, 10),
    }
    return render(request, template_name, context)

def about(request):
    '''Respond to URL 'about', delegate work to a tamplate.'''

    template_name = 'hw/about.html'
    # dict of context variables
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(65, 90)),
        "letter2": chr(random.randint(65, 90)),
        "number": random.randint(1, 10),
    }
    return render(request, template_name, context)


