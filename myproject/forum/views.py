from rest_framework import viewsets
from .models import User, Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer



'''
Views.py answers what to do with requests, how to work with them
Here I use data in JSON and not in HTML
'''


class UserView(viewsets.ModelViewSet):  # viewsets.ModelViewSet - This is a class from DRF that automatically creates a full set of actions (CRUD)
    queryset = User.objects.all()
    serializer_class = UserSerializer  # Blue circles is not scare. I'm overriding an attribute that already exists in the parent class, but that's how it should be

class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class LikeView(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
