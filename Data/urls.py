from django.conf.urls import url
from django.contrib import admin

from Data.views import GetCurrentData, PostData, GetListRange, GetAverageRange

urlpatterns = [
    url(r'current', GetCurrentData),
    url(r'push', PostData),
    url(r'list/range', GetListRange),
    url(r'average/range', GetAverageRange),

]