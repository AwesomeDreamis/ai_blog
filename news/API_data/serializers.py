from app_news_board.models import News, Images, Comment
from app_users.models import Profile
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_staff', 'username', 'email', 'first_name', 'last_name', 'profile', ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'profile_img', 'profile_head_img', 'is_banned', 'news_count', 'sub_count', 'subscribers', 'subs_count', 'subscriptions']


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'views_count', 'is_active', 'total_likes', 'likes', 'saves']


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'news', 'image', ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'news', 'user', 'text', 'image', 'created_at', ]
