# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 23:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0005_remove_fishingevent_completeddatetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fishingevent',
            name='eventVersion',
        ),
    ]
