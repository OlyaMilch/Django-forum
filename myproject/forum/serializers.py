from rest_framework import serializers
from .models import UserProfile, Post, Like, Comment
from django.contrib.auth.models import User


'''
2 classes: external (UserSerializer) is the serializer itself for converting objects to JSON.
Internal(Meta) is a utility subclass that knows which model to serialize and which fields to use.
'''


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'nickname', 'avatar', 'sex']

class PostSerializer(serializers.ModelSerializer):  # Automatically generates a serializer based on the model
    class Meta:
        model = Post
        fields = '__all__'  # List of fields you want to see in JSON or list ['id', 'title', 'text', 'author']
        read_only_fields = ['author']


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

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Display Security (password is not visible)

    class Meta:
        model = User  # We use the built-in User module, not my model!
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user
