from django.conf.urls import url
from django.contrib import admin

from User.views import PostLogin, GetProfile, PostRegister

urlpatterns = [
    url(r'login', PostLogin),
    url(r'profile', GetProfile),
    url(r'register', PostRegister),
]