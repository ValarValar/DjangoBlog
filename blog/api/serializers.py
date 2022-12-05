from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Post, Profile


class PostSerializer(serializers.ModelSerializer):
    """
        Create post serializer
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'created', 'owner']
        read_only_fields = ('created',)


class ProfileSerializer(serializers.ModelSerializer):
    """
        User profile serializer. Returns only users list of subscriptions
    """
    subscriptions = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['subscriptions']


class UserListSerializer(serializers.ModelSerializer):
    """
        User list serializer
    """
    posts_count = serializers.IntegerField()
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'posts_count', 'profile']


class PostDetailSerializer(serializers.ModelSerializer):
    """
        Post detail serializer
    """
    mark_seen_link = serializers.SerializerMethodField()
    seen = serializers.BooleanField()

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'created', 'owner', 'seen', 'mark_seen_link']
        read_only_field = ("__all__",)

    def get_mark_seen_link(self, obj) -> str:
        """
            returns link to endpoint that marks post as seen
        :param obj:
        :return:
        """
        result = '{}'.format(
            reverse('mark_seen', args=[obj.id], request=self.context['request']))
        return result


class UserPostsSerializer(serializers.ModelSerializer):
    """
        User post serializer. Returns user's detailed post data
    """
    post_fields = ('id', 'title', 'body', 'created', 'owner', 'mark_seen_link')
    posts = PostDetailSerializer(many=True, fields=post_fields)

    class Meta:
        model = User
        fields = ['username', 'posts']
