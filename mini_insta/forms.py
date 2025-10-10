# File: mini_insta/forms.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 10/3/2025
# Descriptipm: define the forms used for create/update/delete operations

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to create new posts for a profile'''

    class Meta:
        '''associate form with database model'''

        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update an existing profile'''
    class Meta:
        '''associate form with database model'''

        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']

class UpdatePostForm(forms.ModelForm):
    '''A form to update an existing post'''
    class Meta:
        '''associate form with database model'''

        model = Post
        fields = ['caption']

