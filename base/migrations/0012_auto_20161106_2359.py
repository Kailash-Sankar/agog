# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-06 18:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_auto_20161106_2358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='parent_id',
            new_name='parent',
        ),
    ]
