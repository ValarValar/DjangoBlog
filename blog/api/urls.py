from django.urls import path

from .views import PostCreateView, UserListView, UserPostsListView, SubcribeView, FeedView

urlpatterns = [
    path('post_create/', PostCreateView.as_view()),
    path('profiles_list/', UserListView.as_view()),
    path('<str:username>/posts/', UserPostsListView.as_view()),
    path('<str:username>/subscribe/', SubcribeView.as_view()),
    path('feed/', FeedView.as_view())
]
