from rest_framework import serializers, viewsets, filters
from reporting.models import Trip, FishingEvent, Species, FishCatch, NonFishingEvent,\
    Port, ProcessedState, Vessel, Organisation, User
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response



class MyOrganisationFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if user.organisation:
            return queryset.filter(organisation=user.organisation)
        else:
            return queryset # for staff/superuser


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


class UserViewSet(MyOrganisationMixIn, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SpeciesSerializer(serializers.ModelSerializer):

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


class PortSerializer(MyOrganisationMixIn, serializers.ModelSerializer):

    class Meta:
        model = Port
        fields = (
            "id",
            "name",
            "location",
        )
    # TODO owner = serializers.ReadOnlyField(source='owner.username')

class PortViewSet(MyOrganisationMixIn, viewsets.ModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PortSerializer


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


class VesselSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vessel
        fields = (
            "id",
            "name",
            "registration",
        )


class VesselViewSet(MyOrganisationMixIn, viewsets.ModelViewSet):
    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer


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


class ProcessedStateViewSet(viewsets.ModelViewSet):
    queryset = ProcessedState.objects.all()
    serializer_class = ProcessedStateSerializer


# Serializers define the API representation.
class FishCatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = FishCatch
        fields = ("species", "weightKgs")


# ViewSets define the view behavior.
class FishCatchViewSet(viewsets.ModelViewSet):
    queryset = FishCatch.objects.all()
    serializer_class = FishCatchSerializer


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


class FishingEventSerializer(MyUserMixIn, serializers.ModelSerializer):

    fishCatches = serializers.PrimaryKeyRelatedField(many=True, queryset=FishCatch.objects.all())

    class Meta:
        model = FishingEvent
        fields = fishingEventFields

class FishingEventSubmitSerializer(MyUserMixIn, serializers.ModelSerializer):

    def create(self, validated_data):
        fishCatchData = validated_data.pop('fishCatches')
        fishingEvent = FishingEvent.objects.create(**validated_data)
        for fishCatch_data in fishCatchData:
            FishCatch.objects.create(fishingEvent=fishingEvent, **fishCatch_data)
        return fishingEvent

    class Meta:
        model = FishingEvent
        fields = fishingEventFields


class FishingEventExpandSerializer(MyUserMixIn, serializers.ModelSerializer):

    fishCatches = FishCatchSerializer(many=True)

    class Meta:
        model = FishingEvent
        fishingEventFields = fishingEventFields


class FishingEventViewSet(MyOrganisationMixIn, viewsets.ModelViewSet):

    queryset = FishingEvent.objects.all()
    serializer_class = FishingEventSerializer

    @detail_route(methods=['get'])
    def expanded(self, request, pk=None):
        serializer = FishingEventExpandSerializer(data=request.data)
        serializer.is_valid()
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = FishingEventSubmitSerializer(data=request.data)
        serializer.is_valid()
        return Response(serializer.data)



class OrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisation
        fields = ("id", "fullName")


class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer


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
    "fishingEvents",
)


class TripSerializer(MyOrganisationMixIn, MyUserMixIn, serializers.ModelSerializer):

    fishingEvents = serializers.PrimaryKeyRelatedField(many=True, queryset=FishingEvent.objects.all())

    class Meta:
        model = Trip
        fields = tripFields


class TripExpandSerializer(MyOrganisationMixIn, MyUserMixIn, serializers.ModelSerializer):

    fishingEvents = FishingEventViewSet(many=True, queryset=FishingEvent.objects.all())

    class Meta:
        model = Trip
        fields = tripFields


class TripViewSet(MyOrganisationMixIn, viewsets.ModelViewSet):

    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    @detail_route(methods=['get'])
    def expanded(self, request, pk=None):
        serializer = TripExpandSerializer(data=request.data)
        serializer.is_valid()
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = TripSerializer(data=request.data)
        serializer.is_valid()
        return Response(serializer.data)