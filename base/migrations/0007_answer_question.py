# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-05 17:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20161103_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.Question'),
            preserve_default=False,
        ),
    ]
