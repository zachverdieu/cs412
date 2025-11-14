# File: dadjokes/admin.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 11/12/2025
# Description: File containing model registration

from django.contrib import admin
from .models import *

admin.site.register(Joke)
admin.site.register(Picture)


