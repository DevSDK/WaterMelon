from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers

from Data.models import RawData, Pipe, HourData


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','date_joined')





