# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 08:45
from __future__ import unicode_literals

from django.db import migrations
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('couchpost', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PendingDocs',
            new_name='PendingDocument',
        ),
        migrations.AddField(
            model_name='pendingdocument',
            name='details',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pendingdocument',
            name='processed',
            field=models.DateTimeField(null=True),
        ),
    ]
