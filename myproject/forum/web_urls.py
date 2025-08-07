from django.urls import path
from .views import post_list_view, register_view, profile_view, login_view, logout_view, post_detail_view, edit_comment_view, delete_comment_view, edit_post_view, delete_post_view, like_post_view


'''
For the HTML forum I create a separate file to separate responsibilities,
otherwise there will be confusion in urls.py
'''


urlpatterns = [
    path('', post_list_view, name='post_list'),  # List of all posts
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('post/<int:pk>/', post_detail_view, name='post_detail'), # One post with details
    path('post/<int:pk>/like/', like_post_view, name='like_post'),
    path('post/<int:pk>/edit/', edit_post_view, name='edit_post'),
    path('post/<int:pk>/delete/', delete_post_view, name='delete_post'),
    path('comment/<int:pk>/edit/', edit_comment_view, name='edit_comment'),
    path('comment/<int:pk>/delete/', delete_comment_view, name='delete_comment'),
]
