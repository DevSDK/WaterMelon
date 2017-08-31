from django.conf.urls import url
from django.contrib import admin

from Pipe.views import GetPipeList, PostPipeAdd, GetPipeInfo

urlpatterns = [
    url(r'list', GetPipeList),
    url(r'add', PostPipeAdd),
    url(r'info', GetPipeInfo),

]