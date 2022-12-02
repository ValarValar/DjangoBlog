from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, Profile


class PostSerializer(serializers.ModelSerializer):
    """
        Сериализатор модели поста
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['title', 'body', 'created', 'owner']
        read_only_fields = ('created',)


class ProfileSerializer(serializers.ModelSerializer):
    """
        Сериализатор модели профиля пользователя.
        Результат список username, на которые подписан пользователь
    """
    subscriptions = serializers.StringRelatedField(many=True)

    class Meta:
        model = Profile
        fields = ['subscriptions']


class UserListSerializer(serializers.ModelSerializer):
    """
        Сериализатор списка пользователей
    """
    posts_count = serializers.SerializerMethodField()
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'posts_count', 'profile']

    def get_posts_count(self, obj):
        """
            Получаем аннотированное поле
            c количеством постом для каждого пользователя
        :param obj:
        :return:
        """
        try:
            return obj.posts__count
        except:
            return None


class UserPostsSerializer(serializers.ModelSerializer):
    """
        Сериализует пользователя, результат
        username и посты пользователя
    """
    posts = PostSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'posts']

