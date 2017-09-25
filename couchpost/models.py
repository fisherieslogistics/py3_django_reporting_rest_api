from django.contrib.gis.db import models
from django.contrib.postgres.fields.jsonb import JSONField
from django.db.models.fields.related import ForeignKey
from django.db.models.deletion import CASCADE
from django.conf import settings


class CouchStatus(models.Model):
    db_name = models.CharField(max_length=250, primary_key=True)
    db_seq = models.CharField(max_length=1024, null=False)


class PostStatus(models.Model):
    table_name = models.CharField(max_length=250, primary_key=True)
    table_timestamp = models.DateTimeField(null=False)


class PendingDocument(models.Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    doc = JSONField()
    imported = models.DateTimeField(null=False, auto_now_add=True)
    process_status = models.CharField(max_length=16, null=True)
    processed = models.DateTimeField(null=True)
    details = models.TextField(null=True)  # error message, etc.
