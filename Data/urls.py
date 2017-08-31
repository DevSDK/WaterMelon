from django.conf.urls import url
from django.contrib import admin

from Data.views import GetCurrentData

urlpatterns = [
    url(r'current/raw', GetCurrentData),

    ]