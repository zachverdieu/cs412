# blog/models.py
# define data models for blog application

from django.db import models
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    '''Encapsulate data of a blog article by another author'''

    # define data attributes of Article object
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    # image_url = models.URLField(blank=True) # url as string
    image_file = models.ImageField(blank=True) # an actual image

    def __str__(self):
        '''return a string representation of this model instance.'''

        return f'{self.title} by {self.author}'
        author: TextField[str]

    def get_absolute_url(self):
        '''return a URL to display one instance of this object'''

        return reverse('blog:article', kwargs={'pk': self.pk})

    def get_all_comments(self):
        '''return a QuerySet of comments about this article'''
        # use object manager to retrieve comments
        comments = Comment.objects.filter(article=self)
        return comments



class Comment(models.Model):
    '''encapsulate idea of a comment about an article'''

    # data attributes for comment
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return string representation of this comment'''

        return f'{self.text}'
