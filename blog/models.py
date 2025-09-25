# blog/models.py
# define data models for blog application

from django.db import models

# Create your models here.
class Article(models.Model):
    '''Encapsulate data of a blog article by another author'''

    # define data attributes of Article object
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''return a string representation of this model instance.'''

        return f'{self.title} by {self.author}'
        author: TextField[str]