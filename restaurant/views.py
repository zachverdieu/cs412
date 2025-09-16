from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random, time

# Create your views here.

def main(request):
    ''' Show main/home page to user'''

    template_name = "restaurant/main.html"

    context = {
        "time": time.ctime(),
    }

    return render(request, template_name, context)

def order(request):
    ''' Show menu/order form for user to submit an order'''

    template_name = "restaurant/order.html"

    context = {
        "time": time.ctime(),
    }

    return render(request, template_name, context)

def confirmation():
    '''Process the form submission, and generate result'''

    return
