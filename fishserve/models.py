from django.contrib.gis.db import models
from django.contrib.postgres.fields.jsonb import JSONField
from django.db.models.deletion import CASCADE
from django.conf import settings


class FishServeEvents(models.Model):
    event_type = models.TextField(null=False)  # tripStart, trawl, etc.
    json = models.TextField(null=False)  # has to be string to avoid formatting changes (it's a signed content)
    headers = JSONField(null=False)
    status = models.CharField(max_length=20, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=CASCADE)
    created = models.DateTimeField(null=False, auto_now_add=True)
    processed = models.DateTimeField(null=True)
    response = models.TextField(null=True)
