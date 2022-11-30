from django.urls import path

from .views import PostCreate, UserList, UserPostsList, SubcribeView

urlpatterns = [
    path('post_create/', PostCreate.as_view()),
    path('profiles_list/', UserList.as_view()),
    path('<str:username>/posts/', UserPostsList.as_view()),
    path('<str:username>/subscribe/', SubcribeView.as_view()),
]
