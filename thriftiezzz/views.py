# File: thriftiezzz/views.py
# Author: Zacharie Verdieu (zverdieu@bu.edu)
# Description: Views for thriftiezzz application

from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from .models import *
from .forms import (
    CreateProfileForm,
    UpdateProfileForm,
    UpdateClothingPostForm,
    CreateClothingPostForm,
    CreateReviewForm,
)

class ClothingPostListView(ListView):
    '''Display all clothing posts in a random order.'''

    model = ClothingPost
    template_name = "thriftiezzz/show_all_clothing_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        '''Return QuerySet of available ClothingPost objects in random order.'''
        return ClothingPost.objects.filter(is_sold=False).order_by('?')


class ProfileListView(ListView):
    '''Display all profiles.'''

    model = Profile
    template_name = "thriftiezzz/show_all_profiles.html"
    context_object_name = "profiles"


class ClothingPostDetailView(DetailView):
    '''Display a single clothing item post.'''

    model = ClothingPost
    template_name = "thriftiezzz/show_clothing_post.html"
    context_object_name = "post"


class ProfileDetailView(DetailView):
    '''Display a single profile.'''

    model = Profile
    template_name = "thriftiezzz/show_profile.html"
    context_object_name = "profile"


class UpdateProfileView(UpdateView):
    '''View to handle update of a profile based on its PK.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "thriftiezzz/update_profile_form.html"
    context_object_name = "profile"


class CreateProfileView(CreateView):
    '''View for creating a new profile.'''

    model = Profile
    form_class = CreateProfileForm
    template_name = "thriftiezzz/create_profile_form.html"
    context_object_name = "profile"

class CreateClothingPostView(CreateView):
    '''Create a new clothing post for a given profile.'''

    model = ClothingPost
    form_class = CreateClothingPostForm
    template_name = "thriftiezzz/create_clothing_post_form.html"
    context_object_name = "post"

    def get_object(self):
        '''Find the Profile this post should be attached to, using pk from the URL.'''

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        return profile

    def get_context_data(self, **kwargs):
        '''Provide the profile context to the template.'''

        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Attach the Profile to the ClothingPost before saving.'''

        profile = self.get_object()
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        '''Redirect to the profile detail page after creating a post.'''

        profile = self.get_object()
        return reverse('thriftiezzz:show_profile', kwargs={'pk': profile.pk})

class UpdateClothingPostView(UpdateView):
    '''View to handle update of a clothing post based on its PK.'''

    model = ClothingPost
    form_class = UpdateClothingPostForm
    template_name = "thriftiezzz/update_clothing_post_form.html"
    context_object_name = "post"


class DeleteClothingPostView(DeleteView):
    '''View class to delete a clothing post.'''

    model = ClothingPost
    template_name = "thriftiezzz/delete_clothing_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        '''Return a dictionary containing context variables for use in this template.'''

        context = super().get_context_data(**kwargs)

        post = self.object
        profile = post.profile

        context['post'] = post
        context['profile'] = profile
        return context

    def get_success_url(self):
        '''Provide URL to redirect to after deleting a post.

        Adjust the reverse() call to match your actual URL names.
        '''
        post = self.object
        return reverse('thriftiezzz:show_prfile', kwargs={'pk': post.profile.pk})


class SearchView(ListView):
    '''View to search for user profiles, posts, and descriptions.'''

    model = Profile
    template_name = "thriftiezzz/search_results.html"
    context_object_name = "profiles"

    def dispatch(self, request, *args, **kwargs):
        '''Handle request; show search form if no query parameter is given.'''

        if 'query' not in request.GET:
            return render(request, "thriftiezzz/search.html")
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''Return QuerySet of Profiles matching the search query.'''

        query = self.request.GET.get('query', '').strip()
        if not query:
            return Profile.objects.none()

        # Basic profile search: username or email contains query
        return Profile.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )

    def get_context_data(self, **kwargs):
        '''Return a dictionary containing context variables for this search.'''

        context = super().get_context_data(**kwargs)

        query = self.request.GET.get('query', '').strip()

        # Clothing posts whose name or description contains the query
        posts = ClothingPost.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ) if query else ClothingPost.objects.none()

        context['query'] = query
        context['posts'] = posts
        context['profiles'] = self.get_queryset()

        return context

class CartDetailView(DetailView):
    '''Display the cart belonging to a given profile.'''

    model = Cart
    template_name = "thriftiezzz/show_cart.html"
    context_object_name = "cart"

    def get_object(self):
        '''Return (or create) the Cart for the Profile whose pk is in the URL.'''

        pk = self.kwargs['pk']               # Profile pk
        profile = Profile.objects.get(pk=pk)
        cart, created = Cart.objects.get_or_create(profile=profile)
        return cart


class AddToCartView(TemplateView):
    '''Add a clothing post to a profile's cart (creating the cart if needed).'''

    def dispatch(self, request, *args, **kwargs):
        '''Handle the request to add a ClothingPost to a Cart.'''

        # pk = Profile pk, post_pk = ClothingPost pk
        profile = Profile.objects.get(pk=kwargs['pk'])
        post = ClothingPost.objects.get(pk=kwargs['post_pk'])

        # Do not allow adding sold items
        if post.is_sold:
            return redirect('thriftiezzz:post', pk=post.pk)

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(profile=profile)
        if not cart.clothing_posts.filter(pk=post.pk).exists():
            cart.clothing_posts.add(post)

        # Redirect to the cart page
        return redirect('thriftiezzz:show_cart', pk=profile.pk)

class CreateReviewView(CreateView):
    '''Create a new review for a clothing post.'''

    model = Review
    form_class = CreateReviewForm
    template_name = "thriftiezzz/create_review_form.html"
    context_object_name = "review"

    def get_object(self):
        '''Return the ClothingPost being reviewed.'''

        post_pk = self.kwargs['post_pk']  # ClothingPost pk from URL
        post = ClothingPost.objects.get(pk=post_pk)
        return post

    def get_context_data(self, **kwargs):
        '''Provide the clothing post in the context.'''

        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post'] = post
        return context

    def form_valid(self, form):
        '''Attach clothing_post, seller, and reviewer profile to the Review.'''

        post = self.get_object()
        # Reviewer profile pk from URL
        profile_pk = self.kwargs['pk']
        reviewer = Profile.objects.get(pk=profile_pk)

        form.instance.clothing_post = post
        form.instance.seller = post.profile
        form.instance.profile = reviewer

        return super().form_valid(form)

    def get_success_url(self):
        '''Redirect back to the clothing post detail page after creating a review.'''

        post = self.get_object()
        return reverse('thriftiezzz:post', kwargs={'pk': post.pk})


class PurchaseClothingPostView(TemplateView):
    '''
    Purchase a clothing post:
    - create a Purchase record
    - mark the post as sold
    - remove it from all carts that contain it
    '''

    def dispatch(self, request, *args, **kwargs):
        '''Handle the purchase of a ClothingPost.'''

        # pk = buyer Profile pk, post_pk = ClothingPost pk
        buyer = Profile.objects.get(pk=kwargs['pk'])
        post = ClothingPost.objects.get(pk=kwargs['post_pk'])

        # Prevent buying your own post
        if buyer == post.profile:
            return redirect('thriftiezzz:post', pk=post.pk)

        # Prevent buying something already sold
        if post.is_sold:
            return redirect('thriftiezzz:post', pk=post.pk)

        # Create purchase record
        Purchase.objects.create(
            buyer=buyer,
            seller=post.profile,
            clothing_post=post,
            amount=post.price,
        )

        # Mark post as sold
        post.is_sold = True
        post.save()

        # Remove from all carts
        Cart.objects.filter(clothing_posts=post).update()
        for cart in Cart.objects.filter(clothing_posts=post):
            cart.clothing_posts.remove(post)

        # Redirect to buyer's profile
        return redirect('thriftiezzz:show_profile', pk=buyer.pk)