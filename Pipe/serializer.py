from rest_framework import serializers

from Data.models import RawData, Pipe, HourData

class PipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipe
        fields = ('id','NickName', 'SetedDate','FK_User')
