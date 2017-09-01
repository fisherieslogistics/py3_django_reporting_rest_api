import uuid
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields.related import ForeignKey


class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullName = models.CharField(max_length=120)


class User(AbstractUser):
    organisation = models.ForeignKey("Organisation", null=True, on_delete=CASCADE)


class FishingEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    RAId = models.CharField(max_length=100, null=True)
    numberInTrip = models.IntegerField(null=True)
    targetSpecies = models.CharField(max_length=50, null=True)
    datetimeAtStart = models.DateTimeField(null=False)
    datetimeAtEnd = models.DateTimeField(null=True)
    committed = models.BooleanField(default=True)
    locationAtStart = models.PointField(geography=True)
    locationAtEnd = models.PointField(geography=True)
    lineString = models.LineStringField(null=True, geography=True)
    eventSpecificDetails = JSONField()
    mitigationDeviceCodes = JSONField(null=True)
    vesselNumber = models.IntegerField()
    isVesselUsed = models.BooleanField(default=True)
    notes = models.TextField(null=True)
    amendmentReason = models.TextField(null=True)
    trip = models.ForeignKey("Trip", null=False, on_delete=CASCADE)
    archived = models.BooleanField(default=False)


class Species(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    speciesType = models.CharField(max_length=20)
    code = models.CharField(max_length=3)
    description = models.CharField(max_length=50, null=True)
    otherNames = models.TextField(max_length=50, null=True)
    fullName = models.CharField(max_length=50, null=True)
    scientificName = models.CharField(max_length=50, null=True)
    image = models.CharField(max_length=50, null=True)


class FishCatch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    species = models.ForeignKey("Species", on_delete=PROTECT)
    weightKgs = models.IntegerField()
    fishingEvent = models.ForeignKey("FishingEvent",
                                     related_name="fishCatches", on_delete=CASCADE)


class Trip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation = models.ForeignKey("Organisation", null=False, on_delete=CASCADE)
    creator = models.ForeignKey("User", null=False, on_delete=CASCADE)
    RAId = models.CharField(max_length=100, null=True)
    personInCharge = models.CharField(max_length=50)
    ETA = models.DateTimeField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    startLocation = models.PointField(geography=True)
    endLocation = models.PointField(geography=True)
    unloadPort = models.ForeignKey("Port", on_delete=PROTECT)
    vessel = models.ForeignKey("Vessel", on_delete=PROTECT)


class Port(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation = models.ForeignKey("Organisation", null=False, on_delete=CASCADE)
    name = models.CharField(max_length=50)
    location = models.PointField(geography=True)


class NonFishingEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seabirdCaptureCode = models.CharField(max_length=3)
    nonFishProtectedSpecies = models.ForeignKey("Species", on_delete=PROTECT)
    estimatedWeightKg = models.DecimalField(decimal_places=4, max_digits=12)
    numberUninjured = models.IntegerField(null=True)
    numberInjured = models.IntegerField(null=True)
    numberDead = models.IntegerField(null=True)
    tags = JSONField()
    eventHeader = JSONField()
    fishingEvent = models.ForeignKey("FishingEvent", null=True, on_delete=CASCADE)
    trip = models.ForeignKey("Trip", null=False, on_delete=CASCADE)
    isVesselUsed = models.BooleanField()
    completed = models.DateTimeField()
    eventVersion = models.DateTimeField()
    notes = models.TextField()
    completedDateTime = models.DateTimeField()
    amendmentReason = models.TextField()
    archived = models.BooleanField()


class Vessel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    registration = models.IntegerField()
    organisation = models.ForeignKey("Organisation", null=False, on_delete=CASCADE)


class VesselLocation(models.Model):
    vessel = ForeignKey("Vessel", null=False, on_delete=CASCADE)
    timestamp = models.DateTimeField(null=False)
    location = models.PointField(geography=True, null=False)
    
    class Meta:
        # this workaround is here because django doesn't support composite primary key.
        # https://code.djangoproject.com/wiki/MultipleColumnPrimaryKeys
        indexes = [
            models.Index(fields=['vessel', 'timestamp']),
        ]
        unique_together = (("vessel", "timestamp"),)


class ProcessedState(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=3)
    fullName = models.CharField(max_length=50)
    species = models.ForeignKey("Species", on_delete=PROTECT)
    conversionFactor = models.DecimalField(decimal_places=4, max_digits=12)
