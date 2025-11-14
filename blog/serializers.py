# File: blog/serializers.py
# Author: Zacharie verdieu
# Description: Converts django data models to text-representation suitable to transmit over HTTP

from rest_framework import serializers
from .models import * 

class ArticleSerializer(serializers.ModelSerializer):
    ''' serializer for the Article model.
    Specify which models/fields to send in API
    '''

    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'text']

    # add methods to customize the Create/Read?Update?delete operations
    def create(self, validated_data):
        '''Override superclass method that handles object creation'''

        print(f'ArticleSerializer.create, validated_data={validated_data}.')
        # # create an Article object
        # article = Article(**validated_data)
        # # attact a FK for User
        # article.user = User.objects.first()
        # # save object to database
        # article.save()
        # # return object instance
        # return article

        # simplified way
        validated_data['user'] = User.objects.first()
        # do create and save all at once
        return Article.objects.create(**validated_data)
