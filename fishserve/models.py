from django.contrib.gis.db import models
from django.contrib.postgres.fields.jsonb import JSONField


class FishServeEvents(models.Model):
    event_type = models.TextField(null=False)  # tripStart, trawl, etc.
    event_id = models.UUIDField(null=False)
    json = models.TextField(null=False)
    headers = JSONField()
    status = models.CharField(max_length=20)
    created = models.DateTimeField(null=False, auto_now_add=True)
    processed = models.DateTimeField(null=True)
    response = models.TextField(null=True)
