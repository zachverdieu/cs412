# File: mini_insta/urls.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/25/2025
# Description: views for mini_insta application
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm

# Create your views here.
class ProfileListView(ListView):
    '''Define a class to show all blog articles'''

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    '''Display a single profile'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

class UpdateProfileView(UpdateView):
    '''View to handle update of a profile based on its PK'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'
    conext_object_name = "profile"

class PostDetailView(DetailView):
    '''Display a single post'''

    model = Post
    template_name = "mini_insta/post.html"
    context_object_name = "post"

class CreatePostView(CreateView):
    '''Create a new post'''

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_success_url(self):
        '''Provide url to redirect to after creating a post'''

        pk = self.kwargs['pk']
        return reverse('mini_insta:show_profile', kwargs={'pk': pk})

    def get_context_data(self):
        '''Return a dictionary containing context variables for use in this template'''

        # superclass method
        context = super().get_context_data()

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''looks up profile object by pk and attaches it to the profile
        attribute of the post'''

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        form.instance.profile = profile
        post = form.save()

        # if image exists, save it as a new instance of photo model attached to post
        
        # image_url = self.request.POST['image_url']
        # if image_url:
        #     photo = Photo(post=post, image_url=image_url)
        #     photo.save()

        files = self.request.FILES.getlist('image')
        for file in files:
            photo = Photo(post=post, image_file=file)
            photo.save()


        return super().form_valid(form)

class DeletePostView(DeleteView):
    '''View class to delete a post on a profile'''

    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        '''Return a dictionary containing context variables for use in this template'''

        # superclass method
        context = super().get_context_data()

        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)

        profile = post.profile

        context['post'] = post
        context['profile'] = profile
        return context

    def get_success_url(self):
        '''Provide url to redirect to after deleting a post'''

        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)


        return reverse('mini_insta:show_profile', kwargs = {'pk': post.profile.pk})

class UpdatePostView(UpdateView):
    '''View to handle update of a post based on its PK'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'
    context_object_name = 'post'

class ShowFollowersDetialView(DetailView):
    '''View to show followers for a profile, provide profile context variable'''

    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

class ShowFollowingDetialView(DetailView):
    '''View to show profiles followed by a profile, provide profile context variable'''

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class PostFeedListView(ListView):
    '''Displays all posts in the feed of a Profile object'''

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "post"

    def get_context_data(self):
        '''Return a dictionary containing context variables for use in this template'''

        # superclass method
        context = super().get_context_data()

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        context['profile'] = profile
        return context
    
class SearchView(ListView):
    '''View to search for user Profiles and Posts'''

    model = Profile
    template_name = "mini_insta/search_results.html"
    context_object_name = "profile"

    def dispatch(self, request, *args, **kwargs):
        '''override super method to handle any request'''

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        if 'query' not in request.GET:
            return render(request, 'mini_insta/search.html', {'profile': profile})
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''returns QuerySet of instance data for this search'''

        query = self.request.GET.get('query', '')
        return Post.objects.filter(caption__contains=query)

    def get_context_data(self):
        '''Return a dictionary containing context variables for use in this template'''

        # superclass method
        context = super().get_context_data()


        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        query = self.request.GET.get('query', '')

        context['profile'] = profile
        if query:
            context['query'] = query
        context['posts'] = self.get_queryset()
        context['profiles'] = Profile.objects.filter(
            Q(username__icontains=query) |
            Q(display_name__icontains=query) |
            Q(bio_text__icontains=query)
        )

        return context