# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-06-12 13:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20180612_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(max_length=60, unique=True),
        ),
    ]
