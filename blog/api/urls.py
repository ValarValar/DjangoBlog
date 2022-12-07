from django.urls import path

from .views import (
    PostCreateView, UserListView, UserPostsListView,
    SubscribeView, FeedView, PostMarkAsSeenView
)

urlpatterns = [
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('profiles_list/', UserListView.as_view(), name='profiles_list'),
    path('<str:username>/posts/', UserPostsListView.as_view(), name='users_posts'),
    path('<str:username>/subscribe/', SubscribeView.as_view(), name='subscribe_on_user'),
    path('post/<int:post_id>/seen/', PostMarkAsSeenView.as_view(),  name='mark_seen'),
    path('feed/', FeedView.as_view(), name='feed')
]
