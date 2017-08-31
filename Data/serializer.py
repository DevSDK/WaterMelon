from rest_framework import serializers

from Data.models import RawData, Pipe, HourData


class RawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawData
        fields = ('Data', 'Temp','FK_Pipe_ID','DateTime')

class HourDataSerializer(serializers.ModelSerializer):
    class Meta:
        models = HourData
        fields = ('Data', 'Temp', 'FK_Pipe_ID', 'DateTime')



class PipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipe
        fields = ('NickName', 'SetedDate','FK_User')
