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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class CurrentProfileMixin:
    """Adds current_profile to the context if the user is logged in."""

    def get_current_profile(self):
        if self.request.user.is_authenticated:
            try:
                return self.request.user.thrift_profile
            except Profile.DoesNotExist:
                return None
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_profile"] = self.get_current_profile()
        return context


class ClothingPostListView(CurrentProfileMixin, ListView):
    '''Display all clothing posts in a random order.'''

    model = ClothingPost
    template_name = "thriftiezzz/show_all_clothing_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        '''Return QuerySet of available ClothingPost objects in random order.'''
        return ClothingPost.objects.filter(is_sold=False).order_by('?')

class ProfileListView(CurrentProfileMixin, ListView):
    '''Display all profiles.'''

    model = Profile
    template_name = "thriftiezzz/show_all_profiles.html"
    context_object_name = "profiles"


class ClothingPostDetailView(CurrentProfileMixin, DetailView):
    '''Display a single clothing item post.'''

    model = ClothingPost
    template_name = "thriftiezzz/show_clothing_post.html"
    context_object_name = "post"

   


class ProfileDetailView(CurrentProfileMixin, DetailView):
    '''Display a single profile.'''

    model = Profile
    template_name = "thriftiezzz/show_profile.html"
    context_object_name = "profile"


class UpdateProfileView(CurrentProfileMixin, LoginRequiredMixin, UpdateView):
    '''View to handle update of a profile based on its PK.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "thriftiezzz/update_profile_form.html"
    context_object_name = "profile"


class CreateProfileView(CurrentProfileMixin, CreateView):
    '''View for creating a new profile.'''

    model = Profile
    form_class = CreateProfileForm
    template_name = "thriftiezzz/create_profile_form.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        '''Return a dictionary containing context variables for use in this template'''

        # superclass method
        context = super().get_context_data(**kwargs)

        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        '''creates a new user object in addition to the profile created upon form submission'''

        # reconstruct UserCreationForm instance
        user_form = UserCreationForm(self.request.POST)
        
        # Validate the user form
        if not user_form.is_valid():
            # Add user_form back to context with errors
            context = self.get_context_data(form=form)
            context['user_form'] = user_form  # Include the form with errors
            return self.render_to_response(context)
        
        # save the UserCreationForm to get the new user
        user = user_form.save()
        
        # Log the User in
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        # attach django User to Profile instance object
        form.instance.user = user
        
        # Copy username from User to Profile if needed
        form.instance.username = user.username

        return super().form_valid(form)

    def get_success_url(self):
        '''Redirect to the newly created profile page after submission.'''

        return reverse('thriftiezzz:show_profile', kwargs={'pk': self.object.pk})

class CreateClothingPostView(CurrentProfileMixin, LoginRequiredMixin, CreateView):
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

class UpdateClothingPostView(CurrentProfileMixin, LoginRequiredMixin, UpdateView):
    '''View to handle update of a clothing post based on its PK.'''

    model = ClothingPost
    form_class = UpdateClothingPostForm
    template_name = "thriftiezzz/update_clothing_post_form.html"
    context_object_name = "post"


class DeleteClothingPostView(CurrentProfileMixin, LoginRequiredMixin, DeleteView):
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
        return reverse('thriftiezzz:show_profile', kwargs={'pk': post.profile.pk})


class SearchView(CurrentProfileMixin, ListView):
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

class CartDetailView(CurrentProfileMixin, LoginRequiredMixin, DetailView):
    '''Display the cart belonging to a given profile.'''

    model = Cart
    template_name = "thriftiezzz/show_cart.html"
    context_object_name = "cart"

    def get_object(self):
        '''Return (or create) the Cart for the Profile whose pk is in the URL.'''

        pk = self.kwargs['pk']              
        profile = Profile.objects.get(pk=pk)
        cart, created = Cart.objects.get_or_create(profile=profile)
        return cart

    def post(self, request, *args, **kwargs):
        '''Handle removal of an item from the cart.'''
        cart = self.get_object()
        post_id = request.POST.get("post_id")

        if post_id:
            try:
                post = ClothingPost.objects.get(pk=post_id)
                cart.clothing_posts.remove(post)
            except ClothingPost.DoesNotExist:
                pass  # silently ignore bad IDs

        # Redirect back to the same cart page
        return redirect('thriftiezzz:show_cart', pk=cart.profile.pk)


class AddToCartView(CurrentProfileMixin, LoginRequiredMixin, TemplateView):
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

class CreateReviewView(CurrentProfileMixin, LoginRequiredMixin, CreateView):
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
        return reverse('thriftiezzz:show_clothing_post', kwargs={'pk': post.pk})


class PurchaseView(CurrentProfileMixin, LoginRequiredMixin, TemplateView):
    """
    Handles:
    - Purchasing ONE clothing post (if post_pk is provided)
    - Purchasing ALL items in a user's cart (if only pk is provided)
    Uses the SAME purchase.html template.
    """

    template_name = "thriftiezzz/purchase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = Profile.objects.get(pk=kwargs["pk"])
        context["buyer"] = profile  # always include buyer

        post_pk = kwargs.get("post_pk")

        # CASE 1: Single item purchase
        if post_pk:
            post = ClothingPost.objects.get(pk=post_pk)
            context["post"] = post
            return context

        # CASE 2: Cart purchase
        cart, _ = Cart.objects.get_or_create(profile=profile)
        context["cart"] = cart
        return context

    def post(self, request, *args, **kwargs):
        """Handles the actual purchase submission."""

        buyer = Profile.objects.get(pk=kwargs["pk"])
        post_pk = kwargs.get("post_pk")

        # ============================
        # CASE 1 — PURCHASE ONE POST
        # ============================
        if post_pk:
            post = ClothingPost.objects.get(pk=post_pk)

            # Prevent buying your own item
            if post.profile == buyer:
                return redirect("thriftiezzz:post", pk=post.pk)

            # Prevent double-purchase
            if post.is_sold:
                return redirect("thriftiezzz:post", pk=post.pk)

            # Create Purchase entry
            Purchase.objects.create(
                buyer=buyer,
                seller=post.profile,
                clothing_post=post,
                amount=post.price
            )

            # Mark item sold
            post.is_sold = True
            post.save()

            # Remove from all carts
            for cart in Cart.objects.filter(clothing_posts=post):
                cart.clothing_posts.remove(post)

            # Update buyer stats
            buyer.num_purchases += 1
            buyer.save()

            return redirect("thriftiezzz:show_profile", pk=buyer.pk)

        # ============================
        # CASE 2 — PURCHASE ENTIRE CART
        # ============================
        cart, _ = Cart.objects.get_or_create(profile=buyer)
        items = list(cart.clothing_posts.all())

        if not items:
            # nothing to purchase
            return redirect("thriftiezzz:show_cart", pk=buyer.pk)

        purchased = 0
        for item in items:
            # Skip sold items
            if item.is_sold:
                continue

            # Create Purchase entry
            Purchase.objects.create(
                buyer=buyer,
                seller=item.profile,
                clothing_post=item,
                amount=item.price
            )

            # Mark sold
            item.is_sold = True
            item.save()

            # Remove from carts globally
            for other_cart in Cart.objects.filter(clothing_posts=item):
                other_cart.clothing_posts.remove(item)

            purchased += 1

        # Update profile stats
        buyer.num_purchases += purchased
        buyer.save()

        # Clear cart
        cart.clothing_posts.clear()

        return redirect("thriftiezzz:show_profile", pk=buyer.pk)

class LogoutConfirmationView(CurrentProfileMixin, TemplateView):
    '''view to display logout confirmation page'''

    template_name = "thriftiezzz/logged_out.html"


