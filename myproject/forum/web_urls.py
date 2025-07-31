from django.urls import path
from .views import post_list_view, register_view, profile_view, login_view, logout_view


'''
For the HTML forum I create a separate file to separate responsibilities,
otherwise there will be confusion in urls.py
'''


urlpatterns = [
    path('', post_list_view, name='post_list'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('post/<int:pk>/', post_detail_view, name='post_detail'),
]
