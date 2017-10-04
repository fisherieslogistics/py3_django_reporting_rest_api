import uuid
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.contrib.postgres.fields.array import ArrayField


class ExtraInfoMixIn(models.Model):
    extra_info = JSONField(null=True)

    class Meta:
        abstract = True

    def update_extra_info(self, d):
        if self.extra_info is None:
            self.extra_info = {}
        self.extra_info.update(d)


class Organisation(ExtraInfoMixIn, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullName = models.CharField(max_length=120)

    def __str__(self):
        return self.fullName


class User(ExtraInfoMixIn, AbstractUser):
    organisation = models.ForeignKey("Organisation", null=True, on_delete=CASCADE)

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.email


class ReplicationReadyModel(models.Model):
    class Meta:
        abstract = True

    # this adds fields necessary for couchpost to be able to replicate data to couchdb
    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)
    active = models.BooleanField(null=False, default=True)


class FishingEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    RAId = models.CharField(max_length=100, null=True)
    numberInTrip = models.IntegerField(null=True)
    targetSpecies = models.ForeignKey("Species", on_delete=CASCADE, null=True)
    datetimeAtStart = models.DateTimeField(null=True)
    datetimeAtEnd = models.DateTimeField(null=True)
    committed = models.BooleanField(default=True)
    locationAtStart = models.PointField(geography=True, null=True)
    locationAtEnd = models.PointField(geography=True, null=True)
    lineString = models.LineStringField(null=True, geography=True)
    eventSpecificDetails = JSONField()
    mitigationDeviceCodes = JSONField(null=True)
    vesselNumber = models.IntegerField()
    isVesselUsed = models.BooleanField(default=True)
    notes = models.TextField(null=True)
    amendmentReason = models.TextField(null=True)
    trip = models.ForeignKey("Trip", null=False, on_delete=CASCADE, related_name="fishingEvents")
    creator = models.ForeignKey("User", null=False, on_delete=CASCADE)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s" % (self.trip.vessel.name, self.datetimeAtStart)


class Species(ReplicationReadyModel):
    code = models.CharField(max_length=3, primary_key=True, editable=False)
    speciesType = models.CharField(max_length=20)
    description = models.CharField(max_length=50, null=True)
    otherNames = models.TextField(max_length=50, null=True)
    fullName = models.CharField(max_length=50, null=True)
    scientificName = models.CharField(max_length=50, null=True)
    image = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.code


class FishCatch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    species = models.ForeignKey("Species", on_delete=CASCADE)
    weightKgs = models.IntegerField()
    fishingEvent = models.ForeignKey("FishingEvent",
                                     related_name="fishCatches", on_delete=CASCADE)

    def __str__(self):
        return "%s %s" % (self.species.code, self.fishingEvent.trip.vessel.name)


class Trip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation = models.ForeignKey("Organisation", null=False, on_delete=CASCADE)
    creator = models.ForeignKey("User", null=False, on_delete=CASCADE)
    RAId = models.CharField(max_length=100, null=True)
    personInCharge = models.CharField(max_length=50)
    ETA = models.DateTimeField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    startLocation = models.PointField(geography=True, null=True)
    endLocation = models.PointField(geography=True, null=True)
    unloadPort = models.ForeignKey("Port", on_delete=CASCADE)
    vessel = models.ForeignKey("Vessel", on_delete=CASCADE, related_name="trips")

    def __str__(self):
        return "%s %s" % (self.vessel.name, self.startTime)

    @property
    def totals(self):
        fishCatchSets = [x.fishCatches.all() for x in self.fishingEvents.all()]
        fishCatches = [fc for sublist in fishCatchSets for fc in sublist]
        totals = {}
        for fc in [f for f in fishCatches if f.weightKgs > 0]:
            if fc.species.code in totals:
                totals[fc.species.code] += fc.weightKgs
            else:
                totals[fc.species.code] = fc.weightKgs

        return totals.items()


class Port(ReplicationReadyModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation = models.ForeignKey("Organisation", null=False, on_delete=CASCADE)
    name = models.CharField(max_length=50)
    location = models.PointField(geography=True, null=True)

    def __str__(self):
        return self.name


class NonFishingEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seabirdCaptureCode = models.CharField(max_length=3)
    nonFishProtectedSpecies = models.ForeignKey("Species", on_delete=CASCADE)
    estimatedWeightKg = models.IntegerField(null=True)
    numberUninjured = models.IntegerField(null=True)
    numberInjured = models.IntegerField(null=True)
    numberDead = models.IntegerField(null=True)
    tags = ArrayField(models.CharField(max_length=1024))
    fishingEvent = models.ForeignKey("FishingEvent", null=True, on_delete=CASCADE)
    trip = models.ForeignKey("Trip", null=False, on_delete=CASCADE)
    isVesselUsed = models.BooleanField()
    notes = models.TextField()
    completedDateTime = models.DateTimeField()
    archived = models.BooleanField()


class LandingEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trip = models.ForeignKey("Trip", null=False, on_delete=CASCADE, related_name="landingEvents")
    species = models.ForeignKey("Species", on_delete=CASCADE, null=False)
    landedState = models.CharField(max_length=3, null=False)
    containers = models.IntegerField(null=True)
    containerType = models.CharField(max_length=3, null=True)
    contentWeight = models.IntegerField(null=True)
    destinationType = models.CharField(max_length=1, null=False)
    destinationNumber = models.CharField(max_length=32, null=True)
    greenWeight = models.IntegerField(null=False)
    invoiceNumber = models.CharField(max_length=32, null=True)


class Vessel(ReplicationReadyModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    registration = models.IntegerField()
    organisation = models.ForeignKey("Organisation", null=False, on_delete=CASCADE)

    def __str__(self):
        return self.name


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
    species = models.ForeignKey("Species", on_delete=CASCADE)
    conversionFactor = models.DecimalField(decimal_places=4, max_digits=12)

    def __str__(self):
        return self.code
