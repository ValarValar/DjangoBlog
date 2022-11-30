from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, Post, UserPostRelation

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(UserPostRelation)

