# File: mini_insta/admin.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/25/2025
# Description: File containing model registration

from django.contrib import admin
from .models import Profile, Post, Photo

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)