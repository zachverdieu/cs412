# File: mini_insta/admin.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/25/2025
# Description: File containing model registration

from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)
