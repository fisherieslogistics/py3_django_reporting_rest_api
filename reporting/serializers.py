from rest_framework import serializers, filters
from reporting.models import Trip, FishingEvent, Species, FishCatch, NonFishingEvent,\
    Port, ProcessedState, Vessel, Organisation, User, LandingEvent


class MyOrganisationFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if user.organisation:
            return queryset.filter(organisation=user.organisation)
        else:
            return queryset  # for staff/superuser


class MyOrganisationMixIn():
    filter_backends = (MyOrganisationFilter,)

    def perform_create(self, serializer):
        serializer.validated_data['organisation_id'] = self.request.user.organisation.id
        super().perform_create(serializer)


class MyUserMixIn():

    def perform_create(self, serializer):
        serializer.validated_data['creator_id'] = self.request.user.id
        super().perform_create(serializer)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "organisation",
            "id",
            "username",
            "email",
        )


class SpeciesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Species
        fields = (
            "speciesType",
            "code",
            "description",
            "otherNames",
            "fullName",
            "scientificName",
            "image",
        )


class PortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Port
        fields = (
            "id",
            "name",
            "location",
        )
    # TODO owner = serializers.ReadOnlyField(source='owner.username')


class NonFishEventSerializer(serializers.ModelSerializer):

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
            "fishingEvent",
            "trip",
            "isVesselUsed",
            "notes",
            "completedDateTime",
            "archived",
        )


class VesselSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vessel
        fields = (
            "id",
            "name",
            "registration",
        )


class ProcessedStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProcessedState
        fields = (
            "id",
            "code",
            "fullName",
            "Species",
            "conversionFactor",
        )


class FishCatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = FishCatch
        fields = ("species", "weightKgs")


class LandingEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = LandingEvent
        fields = ("id",  "trip_id", "species", "landedState", "containers", "containerType", "contentWeight",
                  "destinationType", "destinationNumber", "greenWeight", "invoiceNumber")


fishingEventFields = (
    "id",
    "RAId",
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
    "notes",
    "amendmentReason",
    "trip",
    "archived",
    "fishCatches",
)


class FishingEventSubmitSerializer(serializers.ModelSerializer):

    trip = serializers.PrimaryKeyRelatedField(many=False, queryset=Trip.objects.all())
    fishCatches = FishCatchSerializer(many=True)

    class Meta:
        model = FishingEvent
        fields = fishingEventFields


class FishingEventExpandSerializer(serializers.ModelSerializer):

    fishCatches = FishCatchSerializer(many=True)

    class Meta:
        model = FishingEvent
        fields = fishingEventFields + ('locationAtStartGeoJSON', 'locationAtEndGeoJSON', )


class OrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisation
        fields = ("id", "fullName")


tripFields = (
    "RAId",
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


class TripSerializer(serializers.ModelSerializer):

    # TODO remove these - this makes the LIST action slooooooooooow!
    # it has to be some kind of view/custom sql to do it efficiently
    vesselName = serializers.CharField(
        source='vessel.name', read_only=True)
    unloadPortName = serializers.CharField(
        source='unloadPort.name', read_only=True)

    class Meta:
        model = Trip
        fields = tripFields + ("vesselName", "unloadPortName")


class TripExpandSerializer(serializers.ModelSerializer):

    fishingEvents = FishingEventExpandSerializer(many=True)
    landingEvents = LandingEventSerializer(many=True)
    vessel = VesselSerializer(many=False)
    unloadPort = PortSerializer(many=False)
    totals = serializers.ReadOnlyField()

    class Meta:
        model = Trip
        fields = tripFields + ("landingEvents", "fishingEvents", "totals", )


class TripSubmitSerializer(serializers.ModelSerializer):
    unloadPort = serializers.PrimaryKeyRelatedField(many=False, queryset=Port.objects.all())
    vessel = serializers.PrimaryKeyRelatedField(many=False, queryset=Vessel.objects.all())

    class Meta:
        model = Trip
        fields = tripFields
