# File: mini_insta/urls.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/25/2025
# Description: views for mini_insta application
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin ##for authorization
from django.contrib.auth.forms import UserCreationForm ## for new User
from django.contrib.auth.models import User ## django user model
from django.contrib.auth import login



# Create your views here.
class ProfileListView(ListView):
    '''Define a class to show all profiles'''

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    '''Display a single profile'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        '''method to find Profile object for this model instance'''

        # if no pk in kwargs, return logged-in user instead
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            profile = Profile.objects.get(pk=pk)
        else:
            user = self.request.user
            profile = Profile.objects.get(user=user)
        return profile

    def get_context_data(self, **kwargs):
        ''' allows me to use current_profile within template'''
        
        context = super().get_context_data(**kwargs)
        # current_profile is the Profile of the logged-in user
        context['current_profile'] = Profile.objects.get(user=self.request.user)
        return context

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''View to handle update of a profile based on its PK'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'
    conext_object_name = "profile"

    def get_object(self):
        '''method to find Profile object for this model instance'''

        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile

    def get_login_url(self):
        '''return URL for login page when trying to update profile but not logged in'''

        return reverse('mini_insta:login')

class CreateProfileView(CreateView):
    '''view for creating a new profile'''

    model = Profile
    template_name = "mini_insta/create_profile_form.html"
    context_object_name = "profile"
    form_class = CreateProfileForm

    def get_context_data(self, **kwargs):
        '''Return a dictionary containing context variables for use in this template'''

        # superclass method
        context = super().get_context_data()

        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        '''creates a new user object in addition to the profile created upon form submission'''

        # reconstruct UserCreationForm instance
        user_form = UserCreationForm(self.request.POST)
        # save the UserCreationForm to get the new user
        user = user_form.save()
        # Log the User in
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        # attach django User to Profile instance object
        form.instance.user = user

        return super().form_valid(form)
       

class PostDetailView(DetailView):
    '''Display a single post'''

    model = Post
    template_name = "mini_insta/post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        '''supplies context variables for this view'''

        context = super().get_context_data(**kwargs)

        current_profile = Profile.objects.get(user=self.request.user)
        post = Post.objects.get(pk = self.kwargs['pk'])
        # checks if there exists a like object for this post where profile = current profile
        has_liked = post.get_likes().filter(profile=current_profile).exists()
        context['has_liked'] = has_liked
        return context
        

class CreatePostView(LoginRequiredMixin, CreateView):
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

        # use get_object instead of using pk
        profile = self.get_object()

        context['profile'] = profile
        return context

    def get_login_url(self):
        '''return URL for login page when trying to create a post but not logged in'''

        return reverse('blog:login')

    def form_valid(self, form):
        '''looks up profile object by pk and attaches it to the profile
        attribute of the post'''

        # use get_object instead of using pk
        profile = self.get_object()

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

    def get_object(self):
        '''method to find Profile object for this model instance'''

        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile

class DeletePostView(LoginRequiredMixin, DeleteView):
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

    def get_login_url(self):
        '''return URL for login page when trying to delete a post but not logged in'''

        return reverse('blog:login')

class UpdatePostView(LoginRequiredMixin, UpdateView):
    '''View to handle update of a post based on its PK'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'
    context_object_name = 'post'

    def get_login_url(self):
        '''return URL for login page when trying to update a post but not logged in'''

        return reverse('blog:login')

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

class PostFeedListView(LoginRequiredMixin, ListView):
    '''Displays all posts in the feed of a Profile object'''

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "post"

    def get_context_data(self):
        '''Return a dictionary containing context variables for use in this template'''

        # superclass method
        context = super().get_context_data()

        # use get_object instead of using pk
        profile = self.get_object()

        context['profile'] = profile
        return context

    def get_object(self):
        '''method to find Profile object for this model instance'''

        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile

    def get_login_url(self):
        '''return URL for login page when trying to view feed but not logged in'''

        return reverse('blog:login')
    
class SearchView(LoginRequiredMixin, ListView):
    '''View to search for user Profiles and Posts'''

    model = Profile
    template_name = "mini_insta/search_results.html"
    context_object_name = "profile"

    def dispatch(self, request, *args, **kwargs):
        '''override super method to handle any request'''

        # use get_object instead of pk
        profile = self.get_object()

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


        # use get_object instead of pk
        profile = self.get_object()
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

    def get_object(self):
        '''method to find Profile object for this model instance'''

        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile

    def get_login_url(self):
        '''return URL for login page when trying to search but not logged in'''

        return reverse('mini_insta:login')

class LogoutConfirmationView(TemplateView):
    '''view to display logout confirmation page'''

    template_name = "mini_insta/logged_out.html"

class FollowProfileView(LoginRequiredMixin, TemplateView):
    '''view for following a profile'''

    def dispatch(self, request, *args, **kwargs):
        '''handles request for following a profile'''

        target_profile = Profile.objects.get(pk=kwargs['pk'])
        current_profile = Profile.objects.get(user=self.request.user)

        if current_profile != target_profile:
            follow = Follow(follower_profile=current_profile, profile=target_profile)
            follow.save()
        url = reverse('mini_insta:show_profile', kwargs={'pk': target_profile.pk})
        return redirect(url)

class UnFollowProfileView(LoginRequiredMixin, TemplateView):
    ''' view for unfollowing a profile'''

    def dispatch(self, request, *args, **kwargs):
        '''deletes actual instance of the follow'''

        target_profile = Profile.objects.get(pk=kwargs['pk'])
        current_profile = Profile.objects.get(user=self.request.user)

        follow = Follow.objects.filter(follower_profile=current_profile, profile=target_profile)
        follow.delete()
        url = reverse('mini_insta:show_profile', kwargs={'pk': target_profile.pk})
        return redirect(url)

class LikePostView(LoginRequiredMixin, TemplateView):
    '''view for liking a post'''

    def dispatch(self, request, *args, **kwargs):
        '''handles request for liking a post'''

        post = Post.objects.get(pk=kwargs['pk'])
        current_profile = Profile.objects.get(user=self.request.user)

        if post.profile != current_profile:
            this_like = Like(profile=current_profile, post=post)
            this_like.save()
        url = reverse('mini_insta:post', kwargs={'pk': post.pk})
        return redirect(url)

class UnLikePostView(LoginRequiredMixin, TemplateView):
    '''view for unliking a post'''

    def dispatch(self, request, *args, **kwargs):
        '''deletes actual instance of this like'''

        post = Post.objects.get(pk=kwargs['pk'])
        current_profile = Profile.objects.get(user=self.request.user)

        this_like = Like.objects.filter(profile=current_profile, post=post)
        this_like.delete()
        url = reverse('mini_insta:post', kwargs={'pk': post.pk})
        return redirect(url)