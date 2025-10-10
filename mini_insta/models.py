# File: mini_insta/models.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/25/2025
# Description: File creating models for mini_insta
from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    '''Encapsulate data of an user's instagram profile'''

    # define data attributes of Profile object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance'''

        return f'{self.display_name}'

    def get_all_posts(self):
        '''return QuerySet of posts for this profile'''

        posts = Post.objects.filter(profile=self)
        return posts

    def get_absolute_url(self):
        '''return URL to display 1 instance of thsi object'''

        return reverse('mini_insta:show_profile', kwargs = {'pk': self.pk})

class Post(models.Model):
    '''Encapsulate idea of a post to a user's profile'''

    # define data attributes of Post
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=False)

    def __str__(self):
        '''return string representation of post'''
        
        return f'{self.caption}'

    def get_all_photos(self):
        '''return QuerySet of photos for this post'''

        photos = Photo.objects.filter(post=self)
        return photos

class Photo(models.Model):
    '''Encapsulate idea of an immage associated with a post'''

    # define data attributes of Photo
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        '''return string representation of photo'''
        
        return f'image for {self.post} at {self.timestamp}'

    def get_image_url(self):
        '''Returns URL to this image object'''

        if self.image_url:
            return self.image_url
        else:
            return self.image_file.url




