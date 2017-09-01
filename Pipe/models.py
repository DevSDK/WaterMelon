from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Pipe(models.Model):
    NickName = models.CharField(max_length=255)
    SavedDate = models.DateTimeField(auto_now=True)
    FK_User = models.ForeignKey(User)
