# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-06 06:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_auto_20161106_0403'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='alike',
            unique_together=set([('user', 'answer')]),
        ),
        migrations.AlterUniqueTogether(
            name='qlike',
            unique_together=set([('user', 'question')]),
        ),
    ]