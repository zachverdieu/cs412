# File: mini_insta/urls.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 9/25/2025
# Description: File containing url-to-view mapping for mini_insta application

from django.urls import path
from .views import *

app_name = "mini_insta"

urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('post/<int:pk>', PostDetailView.as_view(), name="post"),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile")
]