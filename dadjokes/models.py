from django.db import models

# Create your models here.

class Joke(models.Model):
    '''Model representing a Joke object'''

    text = models.TextField(blank=True)
    contributor = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string represantation of a joke'''

        return f"{self.contributor}'s joke"

class Picture(models.Model):
    '''Model representing a picture object'''

    image_url = models.URLField(blank=True)
    contributor = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string represantation of a picture'''

        return f"{self.contributor} laugh"