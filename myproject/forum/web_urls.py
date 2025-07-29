from django.urls import path
from .views import post_list_view


'''
For the HTML forum I create a separate file to separate responsibilities,
otherwise there will be confusion in urls.py
'''


urlpatterns = [
    path('', post_list_view, name='post_list'),
]
