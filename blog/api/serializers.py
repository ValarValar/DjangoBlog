from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, Profile


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['title', 'body', 'owner', 'created']
        read_only_fields = ('created',)


class ProfileSerializer(serializers.ModelSerializer):
    subscriptions = serializers.StringRelatedField(many=True)

    class Meta:
        model = Profile
        fields = ['subscriptions']


class UserListSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'posts_count', 'profile']

    def get_posts_count(self, obj):
        try:
            return obj.posts__count
        except:
            return None


class UserPostsSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'posts']
