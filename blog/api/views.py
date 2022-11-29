from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .filters import CustomOrderingFilter
from .models import Post
from .serializers import PostSerializer, UserSerializer


class PostCreate(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserList(ListAPIView):
    queryset = User.objects.prefetch_related('posts')
    filter_backends = [CustomOrderingFilter]
    serializer_class = UserSerializer
    ordering_fields = ['username', 'posts__count']

