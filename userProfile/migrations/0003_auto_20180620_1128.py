# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-20 11:28
from __future__ import unicode_literals

from django.db import migrations, models
import userProfile.models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0002_auto_20180619_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(height_field='height_field', upload_to=userProfile.models.upload_location, width_field='width_field'),
        ),
    ]
