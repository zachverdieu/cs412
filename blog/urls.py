# blog/urls.py
from django.urls import path
from .views import  * #ShowAllView, ArticleView, RandomArticleView
# generic view for authentication/authorization
from django.contrib.auth import views as auth_views

app_name = "blog"

urlpatterns = [
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name="show_all"),
    path('article/<int:pk>', ArticleView.as_view(), name="article"),
    path('article/create', CreateArticleView.as_view(), name="create_article"),
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name="create_comment"),
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name="update_article"),
    path('comment/<int:pk>/delete', DeleteCommentView.as_view(), name="delete_comment"),
    ## authorization related
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='blog:show_all'), name="logout"),
    path('register/', UserRegistrationView.as_view(), name="register"),
]