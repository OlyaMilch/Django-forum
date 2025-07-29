from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserView, PostView, CommentView, LikeView, RegisterView, post_list_view


router = DefaultRouter()  # Create a router that automatically creates URL routes
router.register(r'users', UserView)  # Creates all available routes using UserView
router.register(r'posts', PostView)
router.register(r'comments', CommentView)
router.register(r'likes', LikeView)


'''
here separate list of urlpatterns
myproject/urls.py — "master route distributor"
forum/urls.py — routes for the API forum only
'''


urlpatterns = [
    path('', include(router.urls)),  # DRF API route
    path('register/', RegisterView.as_view(), name='register'),  # Register route
    path('forum/', post_list_view, name='post_list'),  # Html-route
]
