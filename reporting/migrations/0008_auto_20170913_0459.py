# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-13 04:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0007_auto_20170913_0350'),
    ]

    operations = [
        migrations.AddField(
            model_name='port',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='species',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='vessel',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
