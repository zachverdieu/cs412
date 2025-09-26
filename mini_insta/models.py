# File: mini_insta/models.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/25/2025
# Description: File creating models for mini_insta
from django.db import models

# Create your models here.

class Profile(models.Model):
    '''Encapsulate data of an user's instagram profile'''

    # define data attributes of Article object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance'''

        return f'{self.display_name}'
