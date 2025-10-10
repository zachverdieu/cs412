# blog/forms.py
# define the forms used for create/update/delete operations

from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    '''A form to add an Article to database'''

    class Meta: 
        '''associate form with model from database'''

        model = Article
        # fields = ['author', 'title', 'text', 'image_url']
        fields = ['author', 'title', 'text', 'image_file']


class CreateCommentForm(forms.ModelForm):
    '''form to add comment about an article'''

    class Meta:
        '''associate this form with a model from database'''
        model = Comment
        fields = ['author', 'text']

class UpdateArticleForm(forms.ModelForm):
    '''Form to handle update to an Article'''

    class Meta:
        '''associate form with model from database'''
        model = Article
        fields = ['title', 'text']