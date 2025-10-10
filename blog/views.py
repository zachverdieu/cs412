from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse

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

class CreateArticleView(CreateView):
    '''view to handle creation of a new Artice
    (1) display HTML form to user (GET)
    (2) process form submission and store new Article object (POST)'''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
        '''override default method to add debug info'''

        # print out form data
        print(f'CreateArtic;eView.form_valid(): {form.cleaned_data}')

        # delegate work to superclass to do the rest
        return super(). form_valid(form)

class CreateCommentView(CreateView):
    '''view to handle creation of a new comment on an article'''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        '''Provide url to ridirect to after creating a new comment'''

        # create and return URL
        # return reverse('show_all')
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        return reverse('blog:article', kwargs={'pk': pk})

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()
        # find/add the article to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        # add this article into the context dictionary:
        context['article'] = article
        return context
        

    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment
        object before saving it to the database.
        '''
        
		# instrument our code to display form fields: 
        #print(f"CreateCommentView.form_valid: form.cleaned_data={form.cleaned_data}")
        print(form.cleaned_data)
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        # attach this article to the comment
        form.instance.article = article # set the FK
 
 
        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
        #saves form data to DB and gives response

class UpdateArticleView(UpdateView):
    '''View to handle update of an article based on its PK'''

    model = Article
    form_class = UpdateArticleForm
    template_name = 'blog/update_article_form.html'

class DeleteCommentView(DeleteView):
    '''View class to detele a comment on an Article'''

    model = Comment
    template_name = "blog/delete_comment_form.html"
    context_object_name = 'comment'

    def get_success_url(self):
        '''Return the URL to redirect to after successful delete'''
        # find PK for this Comment:
        pk = self.kwargs['pk']
        # find Comment object
        comment = Comment.objects.get(pk=pk)
        # find PK of Article comment is for
        article = comment.article
        return reverse('blog:article', kwargs={'pk': article.pk})
