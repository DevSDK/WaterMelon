# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-01 02:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Pipe', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pipe',
            old_name='SetedDate',
            new_name='SavedDate',
        ),
    ]