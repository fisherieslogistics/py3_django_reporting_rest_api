from django.db import models
from django.contrib.postgres.fields import JSONField

class EventHeader(models.Model):

    id = models.UUIDField(primary_key=True)



class FishingEvent(models.Model):

    id = models.UUIDField(primary_key=True)
    numberInTrip = models.IntegerField(blank=True)
    targetSpecies = models.CharField(max_length=50, blank=True)
    datetimeAtStart = models.DateTimeField(blank=False)
    datetimeAtEnd = models.DateTimeField(blank=True)
    committed = models.BooleanField()
    locationAtStart = JSONField()
    locationAtEnd = JSONField()
    lineString = JSONField()
    eventSpecificDetails = JSONField()
    eventHeader = models.ForeignKey('EventHeader')
    mitigationDeviceCodes = JSONField()
    vesselNumber = models.IntegerField()
    isVesselUsed = models.BooleanField()
    completed = models.DateTimeField()
    eventVersion = models.DateTimeField()
    notes = models.TextField()
    completedDateTime = models.DateTimeField()
    amendmentReason = models.TextField()
    trip = models.ForeignKey('Trip', blank=False)
    archived = models.BooleanField()


class FishSpecies(models.Model):

    id = models.UUIDField(primary_key=True)
    speciesType = models.CharField(max_length=20)
    code = models.CharField(max_length=3)
    description = models.CharField(max_length=50, blank=True)
    otherNames = models.TextField(max_length=50, blank=True)
    fullName = models.CharField(max_length=50, blank=True)
    scientificName = models.CharField(max_length=50, blank=True)
    image = models.CharField(max_length=50, blank=True)


class FishCatch(models.Model):

    id = models.UUIDField(primary_key=True)
    fishSpecies = models.ForeignKey('FishSpecies')
    fishingEvent = models.ForeignKey('FishingEvent')


class Trip(models.Model):

    id = models.UUIDField(primary_key=True)
    personInCharge = models.CharField(max_length=50)
    ETA = models.DateTimeField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    startLocation = JSONField()
    endLocation = JSONField()
    unloadPort = models.ForeignKey('Port')
    vessel = models.ForeignKey('Vessel')


class Port(models.Model):

    id = models.UUIDField(primary_key=True)
    personInCharge = models.CharField(max_length=50)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    startLocation = JSONField()
    endLocation = JSONField()


class NonFishProtectedSpeciesInteractionEvent(models.Model):

    id = models.UUIDField(primary_key=True)
    seabirdCaptureCode = models.CharField(max_length=3)
    nonFishProtectedSpecies = models.ForeignKey('NonFishProtectedSpecies')
    estimatedWeightKg = models.DecimalField(decimal_places=4, max_digits=12)
    numberUninjured = models.IntegerField(blank=True)
    numberInjured = models.IntegerField(blank=True)
    numberDead = models.IntegerField(blank=True)
    tags = JSONField()
    eventHeader = JSONField()
    fishingEvent = models.ForeignKey('FishingEvent', blank=True)
    trip = models.ForeignKey('Trip', blank=True)
    isVesselUsed = models.BooleanField()
    completed = models.DateTimeField()
    eventVersion = models.DateTimeField()
    notes = models.TextField()
    completedDateTime = models.DateTimeField()
    amendmentReason = models.TextField()
    trip = models.ForeignKey('Trip', blank=False)
    archived = models.BooleanField()


class Vessel(models.Model):

    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=50)
    registration = models.IntegerField()


class ProcessedState(models.Model):

    id = models.UUIDField(primary_key=True)
    code = models.CharField(max_length=3)
    fullName = models.CharField(max_length=50)
    fishSpecies = models.ForeignKey('FishSpecies')
    conversionFactor = models.DecimalField(decimal_places=4, max_digits=12)


class FishReciever(models.Model):

    id = models.UUIDField(primary_key=True)
    fullName = models.CharField(max_length=50)

# Create your models here.
