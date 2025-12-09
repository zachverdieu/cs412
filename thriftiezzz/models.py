# File: thriftiezzz/models.py
# Author: Zacharie Verdieu (zverdieu@bu.edu)
# Description: File creating models for thriftiezzz application

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    '''Encapsulate data of a thriftiezzz user profile'''

    # define data attributes of Profile object
    username = models.TextField(blank=True)
    profile_picture = models.ImageField(blank=True)
    email = models.EmailField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    num_posts = models.IntegerField(default=0)
    num_purchases = models.IntegerField(default=0)

    def __str__(self):
        '''return a string representation of this model instance'''

        return f'{self.username}'

    def get_all_posts(self):
        '''Return all ClothingPosts made by this profile.'''

        return ClothingPost.objects.filter(profile=self)

    def get_cart(self):
        '''Return (or create) the cart associated with this profile.'''

        cart, created = Cart.objects.get_or_create(profile=self)
        return cart

    def get_num_posts(self):
        '''Compute number of posts for this profile.'''

        return ClothingPost.objects.filter(profile=self).count()

    def get_num_purchases(self):
        '''Compute number of purchases made by this profile.'''

        return Purchase.objects.filter(buyer=self).count()

    def get_absolute_url(self):
        '''Return the URL to view this profile.'''

        return reverse('thriftiezzz:show_profile', kwargs={'pk': self.pk})

class ClothingPost(models.Model):
    """A clothing item listed as a post."""

    # User who created the post
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.TextField(blank=True)
    description = models.TextField(blank=True)
    picture = models.ImageField(blank=True)
    color = models.TextField(blank=True)
    size = models.TextField(blank=True)
    condition = models.TextField(blank=True)

    price = models.DecimalField(max_digits=6, decimal_places=2)
    post_date = models.DateTimeField(auto_now=True)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.color} - ${self.price} (posted by {self.profile.username})"

    def get_all_photos(self):
        '''Return a list of all photos for this post.'''

        return [self.picture] if self.picture else []

    def get_all_reviews(self):
        '''Return all reviews made on this clothing post.'''

        return Review.objects.filter(clothing_post=self)

    def get_absolute_url(self):
        '''Return the URL to view this clothing post.'''

        return reverse('thriftiezzz:post', kwargs={'pk': self.pk})

    def can_be_purchased(self):
        '''Return True if this post is still available.'''
        
        return not self.is_sold

class Purchase(models.Model):
    '''Encapsulate data of a thriftiezzz purchase'''

    # define data attributes of Purchase object
    buyer = models.ForeignKey(Profile, related_name='buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey(Profile, related_name='seller', on_delete=models.CASCADE)
    clothing_post = models.ForeignKey(ClothingPost, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        '''return a string representation of this model instance'''

        return f'Purchase by {self.buyer.username} - Item: {self.clothing_post.name} - ${self.amount}'

class Cart(models.Model):
    '''Encapsulate data of a thriftiezzz shopping cart'''

    # define data attributes of Cart object
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    clothing_posts = models.ManyToManyField(ClothingPost)

    def __str__(self):
        '''return a string representation of this model instance'''

        return f'Cart of {self.profile.username} with {self.clothing_posts.count()} items'

    def total_items(self):
        '''Return the number of items in the cart.'''

        return self.clothing_posts.count()

    def total_price(self):
        '''Return the total price of all items in the cart.'''

        return sum(post.price for post in self.clothing_posts.all())

class Review(models.Model):
    '''Encapsulate data of a review for a ClothingPost'''

    # define data attributes of Review object
    clothing_post = models.ForeignKey(ClothingPost, on_delete=models.CASCADE)
    seller = models.ForeignKey(Profile, related_name='seller_profile', on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    review_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance'''

        return f'Review by {self.profile.username} for {self.clothing_post.name} - Rating: {self.rating}'