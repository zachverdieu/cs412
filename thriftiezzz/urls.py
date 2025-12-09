# File: thriftiezzz/urls.py
# Author: Zacharie Verdieu (zverdieu@bu.edu)
# Description: URL-to-view mapping for thriftiezzz application

from django.urls import path
from .views import *

app_name = "thriftiezzz"

urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path('profile/create', CreateProfileView.as_view(), name="create_profile"),
    path('posts', ClothingPostListView.as_view(), name="show_all_posts"),
    path('post/<int:pk>', ClothingPostDetailView.as_view(), name="post"),
    path('profile/<int:pk>/create_post', CreateClothingPostView.as_view(), name="create_post"),
    path('post/<int:pk>/update', UpdateClothingPostView.as_view(), name="update_post"),
    path('post/<int:pk>/delete', DeleteClothingPostView.as_view(), name="delete_post"),
    path('search', SearchView.as_view(), name="search"),
    path('profile/<int:pk>/cart', CartDetailView.as_view(), name="show_cart"),
    path('profile/<int:pk>/cart/add/<int:post_pk>', AddToCartView.as_view(), name="add_to_cart"),
    path('profile/<int:pk>/post/<int:post_pk>/review', CreateReviewView.as_view(), name="create_review"),
    path('profile/<int:pk>/post/<int:post_pk>/purchase', PurchaseClothingPostView.as_view(), name="purchase_post"),
]
