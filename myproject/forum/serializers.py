from rest_framework import serializers
from .models import User, Post, Like, Comment


'''
2 classes: external (UserSerializer) is the serializer itself for converting objects to JSON.
Internal(Meta) is a utility subclass that knows which model to serialize and which fields to use.
'''


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'avatar', 'sex']

class PostSerializer(serializers.ModelSerializer):  # Automatically generates a serializer based on the model
    class Meta:
        model = Post
        fields = '__all__'  # List of fields you want to see in JSON or list ['id', 'title', 'text', 'author']


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # We use a serializer to display the author's data (nickname, avatar, etc.)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())  # PyCharm is worried, but in real time everything works

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    answer = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'text', 'answer', 'created_at']
