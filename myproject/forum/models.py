from django.contrib.auth.models import User  # Django built-in model
from django.db import models


# My models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=40, unique=True)  # Be sure to specify the field type in objects in Django ('models.CharField' - or other)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # The folder is created automatically on first boot.
    sex_choice = [
        ('Ж', 'Женский'),
        ('М', 'Мужской'),
    ]
    sex = models.CharField(max_length=1, choices=sex_choice)

    def __str__(self):
        return self.nickname


class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Comment from a specific user
    title = models.CharField(max_length=100)
    text = models.TextField()
    images = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Will show the comment time
    # likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)  # An alternative to a simple like


# A more complex like model for greater possibilities
class Like(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Link to another model
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')  # on_delete=models.CASCADE - if the linked model is deleted, then this object will be deleted too
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Ban on duplicate likes


class Comment(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')  # Comment under a specific post
    author = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    answer = models.ForeignKey(to='self', null=True, blank=True, on_delete=models.CASCADE)  # Reply to comment
    created_at = models.DateTimeField(auto_now_add=True)
