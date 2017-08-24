from rest_framework import serializers, viewsets
from reporting.models import Trip, FishingEvent, Species, FishCatch, FishReciever, NonFishingEvent,\
    Port, ProcessedState, Vessel

class TripSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Trip
        fields = (
        "id",
        "personInCharge",
        "ETA",
        "startTime",
        "endTime",
        "startLocation",
        "endLocation",
        "unloadPort",
        "vessel",
        )


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class SpeciesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Species
        fields = (
        "id",
        "speciesType",
        "code",
        "description",
        "otherNames",
        "fullName",
        "scientificName",
        "image",
        )


class SpeciesViewSet(viewsets.ModelViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


class PortSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Port
        fields = (
        "id",
        "name",
        "location",
        )


class PortViewSet(viewsets.ModelViewSet):
    queryset = Port.objects.all()
    serializer_class  = PortSerializer


class NonFishEventSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = NonFishingEvent
        fields = (
        "id",
        "seabirdCaptureCode",
        "nonFishProtectedSpecies",
        "estimatedWeightKg",
        "numberUninjured",
        "numberInjured",
        "numberDead",
        "tags",
        "eventHeader",
        "fishingEvent",
        "trip",
        "isVesselUsed",
        "completed",
        "eventVersion",
        "notes",
        "completedDateTime",
        "amendmentReason",
        "trip",
        "archived",
        )


class NonFishEventViewSet(viewsets.ModelViewSet):
    queryset = NonFishingEvent.objects.all()
    serializer_class = NonFishEventSerializer


class VesselSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Vessel
        fields = (
        "id",
        "name",
        "registration",
        )


class VesselViewSet(viewsets.ModelViewSet):
    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer


class ProcessedStateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProcessedState
        fields = (
        "id",
        "code",
        "fullName",
        "Species",
        "conversionFactor",
        )


class ProcessedStateViewSet(viewsets.ModelViewSet):
    queryset = ProcessedState.objects.all()
    serializer_class = ProcessedStateSerializer


class FishRecieverSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FishReciever
        fields = (
        "id",
        "fullName",
        )


class FishRecieverViewSet(viewsets.ModelViewSet):
    queryset = FishReciever.objects.all()
    serializer_class = FishRecieverSerializer


class FishingEventSerializer(serializers.HyperlinkedModelSerializer):

    fishCatches = serializers.PrimaryKeyRelatedField(many=True, queryset=FishCatch.objects.all())

    class Meta:
        model = FishingEvent
        fields = (
            "fishCatches",
            "numberInTrip",
            "targetSpecies",
            "datetimeAtStart",
            "datetimeAtEnd",
            "committed",
            "locationAtStart",
            "locationAtEnd",
            "lineString",
            "eventSpecificDetails",
            "mitigationDeviceCodes",
            "vesselNumber",
            "isVesselUsed",
            "completed",
            "eventVersion",
            "notes",
            "completedDateTime",
            "amendmentReason",
            "trip",
            "archived",
        )


class FishingEventViewSet(viewsets.ModelViewSet):
    queryset = FishingEvent.objects.all()
    serializer_class = FishingEventSerializer


# Serializers define the API representation.
class FishCatchSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FishCatch
        fields = ("species", "weightKgs")


# ViewSets define the view behavior.
class FishCatchViewSet(viewsets.ModelViewSet):
    queryset = FishCatch.objects.all()
    serializer_class = FishCatchSerializer
