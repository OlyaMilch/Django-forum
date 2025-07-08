from rest_framework import viewsets
from .models import UserProfile, Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer, RegisterSerializer
from .permissions import ReadOnly, AdminAndOwner
from django.contrib.auth.models import User
from rest_framework import generics



'''
views.py is the glue between the models and the client. It controls what exactly happens when the user makes an HTTP request.
Here I use data in JSON and not in HTML
'''



class UserView(viewsets.ModelViewSet):  # viewsets.ModelViewSet - This is a class from DRF that automatically creates a full set of actions (CRUD)
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer  # Blue circles is not scare. I'm overriding an attribute that already exists in the parent class, but that's how it should be

class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [ReadOnly | AdminAndOwner]  # Restrict access rights to actions on objects

    def perform_create(self, serializer):  # Called automatically when the user sends a POST request
        serializer.save(author=self.request.user)

class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [ReadOnly | AdminAndOwner]  # Author or admin

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Save post with author = current logged in user


class LikeView(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
