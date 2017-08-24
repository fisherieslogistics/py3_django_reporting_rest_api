import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser

class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullName = models.CharField(max_length=120)


class User(AbstractUser):
    organisation = models.ForeignKey("Organisation", null=True)


class FishingEvent(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    RAId = models.CharField(max_length=100, blank=True)
    numberInTrip = models.IntegerField(blank=True)
    targetSpecies = models.CharField(max_length=50, blank=True)
    datetimeAtStart = models.DateTimeField(blank=False)
    datetimeAtEnd = models.DateTimeField(blank=True)
    committed = models.BooleanField(default=True)
    locationAtStart = JSONField()
    locationAtEnd = JSONField()
    lineString = JSONField(null=True)
    eventSpecificDetails = JSONField()
    mitigationDeviceCodes = JSONField(null=True)
    vesselNumber = models.IntegerField()
    isVesselUsed = models.BooleanField(default=True)
    notes = models.TextField(null=True)
    amendmentReason = models.TextField(null=True)
    trip = models.ForeignKey("Trip", null=False)
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
    species = models.ForeignKey("Species")
    weightKgs = models.IntegerField()
    fishingEvent = models.ForeignKey("FishingEvent",
                                     related_name="fishCatches")


class Trip(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    RAId = models.CharField(max_length=100, blank=True)
    personInCharge = models.CharField(max_length=50)
    ETA = models.DateTimeField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    startLocation = JSONField()
    endLocation = JSONField()
    unloadPort = models.ForeignKey("Port")
    vessel = models.ForeignKey("Vessel")


class Port(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    location = JSONField()


class NonFishingEvent(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seabirdCaptureCode = models.CharField(max_length=3)
    nonFishProtectedSpecies = models.ForeignKey("Species")
    estimatedWeightKg = models.DecimalField(decimal_places=4, max_digits=12)
    numberUninjured = models.IntegerField(null=True)
    numberInjured = models.IntegerField(null=True)
    numberDead = models.IntegerField(null=True)
    tags = JSONField()
    eventHeader = JSONField()
    fishingEvent = models.ForeignKey("FishingEvent", null=True)
    trip = models.ForeignKey("Trip", null=True)
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


class ProcessedState(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=3)
    fullName = models.CharField(max_length=50)
    species = models.ForeignKey("Species")
    conversionFactor = models.DecimalField(decimal_places=4, max_digits=12)


class FishReciever(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullName = models.CharField(max_length=50)
    #TODO - is this maybe an organisation?
