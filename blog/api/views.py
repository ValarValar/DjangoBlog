from django.contrib.auth.models import User
from django.db.models import Count, Case, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .filters import PostSeenFilter
from .models import Post, Profile, UserPostRelation
from .paginators import CustomPageNumberPagination
from .serializers import (
    PostSerializer, ProfileSerializer, UserListSerializer, UserPostsSerializer, PostDetailSerializer
)


class BaseJWTAuthenticationView(APIView):
    """
        Inheritance view for authentication require endpoints
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class PostCreateView(CreateAPIView, BaseJWTAuthenticationView):
    """
        Post creation endpoint. Require Authentication
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserListView(ListAPIView):
    """
        User list endpoint. Allows to order by username and posts_count. \n
        Examples: \n
            both filters:  http://127.0.0.1:8000/api/profiles_list/?ordering=-posts_count,-username
            one ascending:  http://127.0.0.1:8000/api/profiles_list/?ordering=posts_count
            without: http://127.0.0.1:8000/api/profiles_list/
    """
    queryset = User.objects.select_related('profile') \
        .prefetch_related('posts') \
        .annotate(posts_count=Count('posts')) \
        .prefetch_related('profile__subscriptions')

    filter_backends = [OrderingFilter]
    serializer_class = UserListSerializer
    ordering_fields = ['username', 'posts_count']


class UserPostsListView(ListAPIView):
    """
        List of user's detailed posts. Ordered by post creation time.
        Starting with the newest ones
    """
    serializer_class = UserPostsSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs['username']).prefetch_related('posts')


class SubscribeView(BaseJWTAuthenticationView):
    """
        Subscribe/unsubscribe endpoint. Require authentication.
        Request param is username you want to subscribe on.
        Subscribes you if u were not before, otherwise unsubscribes you.
        Example: \n
            http://127.0.0.1:8000/api/admin/subscribe/

    """

    def post(self, request, username=None):
        current_profile = Profile.objects.get(user=request.user)
        if request.user.username == username:
            raise ValidationError({"message": f"You can't subcsribe at yourself"})
        try:
            subcribe_to = User.objects.get(username=username)
            if current_profile.subscriptions.filter(id=subcribe_to.id).exists():
                current_profile.subscriptions.remove(subcribe_to)
            else:
                current_profile.subscriptions.add(subcribe_to)
            result = {
                "profile": ProfileSerializer(current_profile).data,
            }
        except Profile.DoesNotExist:
            raise ValidationError({"message": f'User {username} does not exits'})

        return Response(result)


class FeedView(ListAPIView, BaseJWTAuthenticationView):
    """
        Feed endpoint provides you posts of users you subcribed on.

        Require authentication. Pagination - 10 posts per page. \n
        Allows to filter posts by seen param. \n
        Ordered by post creation time. Starting with the newest ones. \n
        For the purpose of optimize sql queries, pagination doesn't know exactly count of pages.\n
        In case where parameter page num > real pages num, so: it always returns last page. \n
        Usage examples: \n
            without filtering:    http://127.0.0.1:8000/api/feed/
            paginataion: http://127.0.0.1:8000/api/feed/?page=2
            pagination with seen filter: http://127.0.0.1:8000/api/feed/?page=2&seen=false
            show only seen posts: http://127.0.0.1:8000/api/feed/?seen=true
    """
    queryset = Post.objects.none()
    serializer_class = PostDetailSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostSeenFilter
    filterset_fields = ['seen']
    ordering = 'created'

    def get_queryset(self):
        subcribed_at_users_list = Profile.objects.filter(user__id=self.request.user.id). \
            select_related('user')[0].subscriptions.all()

        posts = Post.objects.select_related('owner'). \
            filter(owner__in=subcribed_at_users_list). \
            prefetch_related('user_relation'). \
            annotate(seen=Case(
                When(user_relation__user_id=self.request.user.id, then=True),
                default=False, )
            )
        return posts


class PostMarkAsSeenView(BaseJWTAuthenticationView):
    """
        Endpoint allows to mark or unmark post as seen.
        Example: \n
            http://127.0.0.1:8000/api/post/14/seen/
    """

    def post(self, request, post_id=None):
        needed_relation = UserPostRelation.objects.filter(user_id=request.user.id, post_id=post_id)

        if needed_relation.exists():
            needed_relation.delete()
            flag = False
        else:
            needed_relation.create(user_id=request.user.id, post_id=post_id, seen=True)
            flag = True
        result = {
            "post": post_id,
            "seen": flag
        }
        return Response(result)
