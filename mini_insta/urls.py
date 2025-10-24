# File: mini_insta/urls.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/25/2025
# Description: File containing url-to-view mapping for mini_insta application

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = "mini_insta"

urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('post/<int:pk>', PostDetailView.as_view(), name="post"),
    path('profile/create_post', CreatePostView.as_view(), name="create_post"),
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
    path('profile/<int:pk>/followers', ShowFollowersDetialView.as_view(), name="show_followers"),
    path('profile/<int:pk>/following', ShowFollowingDetialView.as_view(), name="show_following"),
    path('profile/feed', PostFeedListView.as_view(), name="show_feed"),
    path('profile/search', SearchView.as_view(), name="search"),
    path('profile/', ProfileDetailView.as_view(), name="show_profile"),
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='mini_insta:logout_confirmation'), name="logout"),
    path('logout_confirmation/', LogoutConfirmationView.as_view(), name='logout_confirmation'),
 
]