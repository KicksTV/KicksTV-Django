# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-06-15 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20180615_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='on_going',
            field=models.BooleanField(default=True),
        ),
    ]