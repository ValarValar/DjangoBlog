from django.urls import path

from .views import PostCreate, UserList

urlpatterns = [
    path('post_create/', PostCreate.as_view()),
    path('profiles_list/', UserList.as_view()),

]
