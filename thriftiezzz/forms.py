# File: thriftiezzz/forms.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 12/6/2025
# Description: define the forms used for create/update/delete operations

from django import forms
from .models import *

class CreateProfileForm(forms.ModelForm):
    '''A form to create a profile'''

    class Meta:
        '''associate form with database model'''

        model = Profile
        fields = ['username', 'email', 'profile_picture']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update an existing profile'''

    class Meta:
        '''associate form with database model'''

        model = Profile
        fields = ['username', 'profile_picture']

class CreateClothingPostForm(forms.ModelForm):
    '''A form to create a clothing post'''

    class Meta:
        '''associate form with database model'''

        model = ClothingPost
        fields = ['name', 'description', 'picture', 'color', 'size', 'condition', 'price']

class UpdateClothingPostForm(forms.ModelForm):
    '''A form to update an existing clothing post'''

    class Meta:
        '''associate form with database model'''

        model = ClothingPost
        fields = ['name', 'description', 'picture', 'color', 'size', 'condition', 'price']

class CreateReviewForm(forms.ModelForm):
    '''A form to create a review for a clothing post'''

    class Meta:
        '''associate form with database model'''

        model = Review
        fields = ['rating', 'comment']