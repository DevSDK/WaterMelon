from django.contrib import admin

# Register your models here.
from Data.models import RawData, HourData

admin.site.register(RawData)
admin.site.register(HourData)
