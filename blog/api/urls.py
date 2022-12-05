from django.urls import path

from .views import (
    PostCreateView, UserListView, UserPostsListView,
    SubscribeView, FeedView, PostMarkAsSeenView
)

urlpatterns = [
    path('post_create/', PostCreateView.as_view()),
    path('profiles_list/', UserListView.as_view()),
    path('<str:username>/posts/', UserPostsListView.as_view()),
    path('<str:username>/subscribe/', SubscribeView.as_view()),
    path('post/<int:post_id>/seen/', PostMarkAsSeenView.as_view(),  name='mark_seen'),
    path('feed/', FeedView.as_view())
]
