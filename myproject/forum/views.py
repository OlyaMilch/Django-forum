from rest_framework import viewsets
from .models import UserProfile, Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer, RegisterSerializer
from .permissions import ReadOnly, AdminAndOwner
from django.contrib.auth.models import User
from rest_framework import generics
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib import messages



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
        username = request.POST['username']  # Unique user login (Built-in User model)
        password = request.POST['password']
        email = request.POST['email']
        nickname = request.POST['nickname']  # Display name (My UserProfile model)

        # Check: email already registered?
        if User.objects.filter(email=email).exists():
            messages.error(request, "Пользователь с таким email уже существует.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, email=email)  #  "user" will be active upon registration

        # Create a user profile with a nickname
        UserProfile.objects.create(user=user, nickname=nickname)

        return redirect('login')  # Redirect to login

    return render(request, 'forum/register.html')

@login_required  # Built-in Django tool. Checks if the user is logged in (then the code will be executed)
def profile_view(request):
    profile = request.user.profile  # Get the profile of the currently logged in user

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
        return redirect('profile')  # After saving, refresh the page

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


@login_required  # Protection from unauthorized users
def post_detail_view(request, pk):  # Get the desired post by its pk (id)
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        comment_text = request.POST.get("comment_text")  # Get the comment text from the form
        if comment_text:
            Comment.objects.create(  # Create a new Comment object associated with this post
                post=post,
                author=request.user.profile,
                text=comment_text,
                created_at=timezone.now()  # Uses the server's local time (because different parts of the world have different times)
            )
            return redirect('post_detail', pk=pk)  # Refresh the page (redirect) to avoid re-submitting the form

    # The post itself is transferred, and comments are pulled in via post.comments.all in the template.
    context = {
        'post': post,
    }
    return render(request, 'post_detail.html', context)  # Shows an HTML page to the user


# Editing post
@login_required
def edit_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    #  Only the author can edit
    if request.user.profile != post.author:
        return HttpResponseForbidden("У вас нет прав на редактирование этого поста.")

    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        image = request.FILES.get('images')

        if title and text:
            post.title = title
            post.text = text
            if image:
                post.images = image
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:

            pass

    context = {
        'post': post
    }
    return render(request, 'edit_post.html', context)


# Delete post
@login_required
def delete_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Author or admin can delete
    if request.user != post.author.user and not request.user.is_superuser:
        return HttpResponseForbidden("У вас нет прав на удаление этого поста.")

    if request.method == "POST":
        post.delete()
        return redirect('post_list')  # Will return to the page with posts


# Editing comment
@login_required
def edit_comment_view(request, pk):  # pk = id primary key. Instead of pk, the comment number is substituted.
    comment = get_object_or_404(Comment, pk=pk)

    # Only the author can edit
    if request.user != comment.author.user:
        return HttpResponseForbidden("У вас нет прав на редактирование этого комментария.")

    if request.method == 'POST':
        new_text = request.POST.get('text')
        if new_text:
            comment.text = new_text
            comment.save()
            return redirect('post_detail', pk=comment.post.pk)  # Redirects the user to another URL

    context = {
        'comment': comment
    }
    return render(request, 'forum/edit_comment.html', context)


# Delete comment
@login_required
@require_POST  # Only POST requests are allowed
def delete_comment_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # Only the author or admin can delete
    if request.user != comment.author.user and not request.user.is_superuser:
        return HttpResponseForbidden("У вас нет прав на удаление этого комментария.")  # Prohibition method

    post_pk = comment.post.pk  # Return user back to post
    comment.delete()
    return redirect('post_detail', pk=post_pk)
