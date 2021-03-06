from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from Pipe.models import Pipe


class RawData(models.Model):
    Data = models.FloatField()
    DateTime =  models.DateTimeField(auto_now=True)
    Temp = models.FloatField()
    FK_Pipe_ID = models.ForeignKey(Pipe)

class HourData(models.Model):
    Data = models.FloatField()
    Temp = models.FloatField()
    FK_Pipe_ID = models.ForeignKey(Pipe)
    DateTime = models.DateTimeField()