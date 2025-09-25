from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import random

# Create your views here.
class ShowAllView(ListView):
    '''Define a class to show all blog articles'''

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

class ArticleView(DetailView):
    '''Display single article'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

class RandomArticleView(DetailView):
    '''Display single randomly selected article'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    # methods
    def get_object(self):
        '''return one instance of Article object at random'''

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article
