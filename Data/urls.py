from django.conf.urls import url
from django.contrib import admin

from Data.views import GetCurrentData, PostData

urlpatterns = [
    url(r'current/raw', GetCurrentData),
    url(r'push', PostData)
]