# File: mini_insta/models.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/25/2025
# Description: File creating models for mini_insta
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    '''Encapsulate data of an user's instagram profile'''

    # define data attributes of Profile object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        '''return a string representation of this model instance'''

        return f'{self.display_name}'

    def get_all_posts(self):
        '''return QuerySet of posts for this profile'''

        posts = Post.objects.filter(profile=self)
        return posts

    def get_absolute_url(self):
        '''return URL to display 1 instance of this object'''

        return reverse('mini_insta:show_profile', kwargs = {'pk': self.pk})

    def get_followers(self):
        '''return a list of Profiles who follow this Profile'''

        follower_set = Follow.objects.filter(profile=self)

        followers = []
        for i in follower_set:
            followers.append(i.follower_profile)

        return followers

    def get_num_followers(self):
        '''return the number of Profiles who follow this Profile'''

        followers = self.get_followers()
        return len(followers)

    def get_following(self):
        '''return a list of Profiles who this Profile is following'''

        follower_set = Follow.objects.filter(follower_profile=self)

        following = []
        for i in follower_set:
            following.append(i.profile)

        return following

    def get_num_following(self):
        '''return the number of Profiles who this Profile is followin'''

        following = self.get_following()
        return len(following)

    def get_post_feed(self):
        '''return a list of posts made by profiles followed by this profile'''

        posts = []
        for profile in self.get_following():
            for post in profile.get_all_posts():
                posts.append(post)

        posts_sorted = sorted(posts, key=lambda p: p.timestamp, reverse=True)
        return posts_sorted


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

    def get_absolute_url(self):
        '''return URL to display 1 instance of this object'''

        return reverse('mini_insta:post', kwargs = {'pk': self.pk})

    def get_all_comments(self):
        '''returns a querySet of all comments for a single Post object'''

        return Comment.objects.filter(post=self)

    def get_likes(self):
        '''return a querySet of all likes on a single Post'''

        return Like.objects.filter(post=self)

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

class Follow(models.Model):
    '''encapsulate the idea of an edge connecting 2 nodes (follow relationship connecting 2 profiles)'''

    # data attributes for follow
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return string representation of follow relationship'''

        return f'{self.follower_profile} follows {self.profile}'

class Comment(models.Model):
    '''encapsulates the idea of one Profile providing a response or commentary on a Post'''

    # data attributes for Comment
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True)

    def __str__(self):
        '''return string representation of comment'''

        return f"{self.profile}'s comment on {self.post.profile}'s post"

class Like(models.Model):
    '''encapsulates the idea of one Profile providing approval of a Post'''

    # data attributes for Like
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return string representation of like'''

        return f"{self.profile} likes {self.post.profile}'s post"