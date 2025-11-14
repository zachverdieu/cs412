# File: dadjokes/serializers.py
# Author: Zacharie Verdieu
# Description: Converts django data models to text-representation suitable to transmit over HTTP

from rest_framework import serializers
from .models import * 

class JokeSerializer(serializers.ModelSerializer):
    ''' serializer for the Joke model.
    Specify which models/fields to send in API
    '''

    class Meta:
        model = Joke
        fields = ['contributor', 'text', 'timestamp']

class PictureSerializer(serializers.ModelSerializer)        :
    ''' serializer for the Picture model.
    Specify which models/fields to send in API
    '''

    class Meta:
        model = Picture
        fields = ['contributor', 'image_url', 'timestamp']