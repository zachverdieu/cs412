# File: thriftiezzz/admin.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 11/25/2025
# Description: File containing model registration

from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(ClothingPost)
admin.site.register(Purchase)
admin.site.register(Cart)
admin.site.register(Review)