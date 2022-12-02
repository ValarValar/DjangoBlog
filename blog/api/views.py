from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Post, Profile
from .paginators import CustomPageNumberPagination
from .serializers import PostSerializer, ProfileSerializer, UserListSerializer, UserPostsSerializer


class BaseJWTAuthetificationView(APIView):
    """
        Доп. класс для наследования  для view требующих аутентификации
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class PostCreateView(CreateAPIView, BaseJWTAuthetificationView):
    """
        Создание поста.
        Необходима аутентификация Bearer access token
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserListView(ListAPIView):
    """
        Список пользователей, использует кастомный сортировочный фильтр,
        который позволяет сортировать по комплексному полю - количество постов
    """
    queryset = User.objects.select_related('profile') \
        .prefetch_related('posts') \
        .annotate(Count('posts')) \
        .prefetch_related('profile__subscriptions')

    filter_backends = [OrderingFilter]
    serializer_class = UserListSerializer
    ordering_fields = ['username', 'posts__count']


class UserPostsListView(ListAPIView):
    serializer_class = UserPostsSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs['username']).prefetch_related('posts')


class SubcribeView(GenericAPIView, BaseJWTAuthetificationView):
    serializer_class = ProfileSerializer

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


class FeedView(ListAPIView, BaseJWTAuthetificationView):
    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination
    ordering = 'created'

    def get_queryset(self):
        subcribed_at_users_list = Profile.objects.filter(user=self.request.user).\
            select_related('user')[0].subscriptions.all()

        posts = Post.objects.select_related('owner').filter(owner__in=subcribed_at_users_list)
        return posts


