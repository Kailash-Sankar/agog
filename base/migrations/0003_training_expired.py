# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-19 11:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20160523_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='expired',
            field=models.BooleanField(default=False),
        ),
    ]
