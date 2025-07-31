from rest_framework import viewsets
from .models import UserProfile, Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer, RegisterSerializer
from .permissions import ReadOnly, AdminAndOwner
from django.contrib.auth.models import User
from rest_framework import generics
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout




'''
views.py is the glue between the models and the client. It controls what exactly happens when the user makes an HTTP request.
Here I use data in JSON and not in HTML
Class - its DRF views!
'''



class UserView(viewsets.ModelViewSet):  # viewsets.ModelViewSet - This is a class from DRF that automatically creates a full set of actions (CRUD)
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer  # Blue circles is not scare. I'm overriding an attribute that already exists in the parent class, but that's how it should be

class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [ReadOnly | AdminAndOwner]  # Restrict access rights to actions on objects

    def perform_create(self, serializer):  # Called automatically when the user sends a POST request
        profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(author=profile)

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

# Django views (for all HTML pages)
def post_list_view(request):
    posts = Post.objects.all().order_by('-created_at')  # Newest posts on top
    return render(request, 'forum/post_list.html', {'posts': posts})

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)  #  "user" will be active upon registration
        return redirect('login')  # Redirect to login

    return render(request, 'forum/register.html')

@login_required
def profile_view(request):
    profile = request.user.profile  # user.profile работает благодаря related_name

    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        sex = request.POST.get('sex')
        avatar = request.FILES.get('avatar')

        # Updating fields (when a user wants changes to the profile)
        profile.nickname = nickname
        profile.sex = sex
        if avatar:
            profile.avatar = avatar

        profile.save()
        return redirect('profile')  # после сохранения — обновить страницу

    return render(request, 'forum/profile.html', {'user': request.user})

# Login
def login_view(request):  # Accepts a request from the user
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me')  # Maybe None

        try:
            user = User.objects.get(email=email)  # Searching for a user by email
        except User.DoesNotExist:  # Else err
            return render(request, 'forum/login.html', {'error': 'Пользователь с такой почтой не найден'})

        user = authenticate(request, username=user.username, password=password)  # We check the password via authenticate(). If the password is correct, it will return the user.
        # If the user exists and the password is correct, log in via login()
        if user is not None:
            login(request, user)

            # If "remember me" is NOT checked, the session will expire when the browser is closed.
            if not remember_me:
                request.session.set_expiry(0)
            return redirect('profile')  # We redirect the user to his profile
        else:
            return render(request, 'forum/login.html', {'error': 'Неверный пароль'})

    return render(request, 'forum/login.html')  # Just showing the login page

def logout_view(request):
    logout(request)  # Ends the session
    return redirect('login')  # Redirect to login (or main page)
