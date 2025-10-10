# File: mini_insta/urls.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/25/2025
# Description: views for mini_insta application
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import *
from .forms import CreatePostForm, UpdateProfileForm

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
