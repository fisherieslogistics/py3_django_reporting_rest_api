from rest_framework import serializers, viewsets, filters
from reporting.models import Trip, FishingEvent, Species, FishCatch, NonFishingEvent,\
    Port, ProcessedState, Vessel, Organisation, User, LandingEvent
from fishserve.models import FishServeEvents
from rest_framework.decorators import detail_route
from rest_framework.response import Response
import datetime
import logging
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin,\
    CreateModelMixin
from rest_framework.viewsets import GenericViewSet


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


class UserViewSet(MyOrganisationMixIn, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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


class SpeciesViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


class PortSerializer(serializers.ModelSerializer):

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


class FishingEventViewSet(MyUserMixIn, CreateModelMixin, GenericViewSet):

    queryset = FishingEvent.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = FishingEventSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['creator_id'] = self.request.user.id
        serializer.validated_data['id'] = request.data['id']
        fishData = serializer.validated_data.pop('fishCatches')
        serializer.save()
        fse = FishServeEvents()

        fse.event_type = request.data['event_type']  # tripStart, trawl, etc.
        fse.json = request.data['json']
        fse.headers = request.data['headers']
        fse.creator = self.request.user
        fse.save()

        for data in fishData:
            FishCatch.objects.create(fishingEvent=serializer.instance, **data)

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


class TripViewSet(MyUserMixIn, MyOrganisationMixIn, viewsets.ModelViewSet):

    queryset = Trip.objects.all().filter(active=True).order_by('-endTime', '-startTime')
    serializer_class = TripSerializer

    @detail_route(methods=['get'])
    def expanded(self, request, pk=None):
        trip = self.get_object()
        serializer = TripExpandSerializer(trip)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def landings(self, request, pk=None):
        trip = self.get_object()
        serializer = LandingEventSerializer(trip.landingEvents, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def add_landing(self, request, pk=None):
        trip = self.get_object()
        serializer = LandingEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #serializer.validated_data['creator_id'] = self.request.user.id
        serializer.validated_data['trip_id'] = trip.id
        serializer.save()
        return Response(serializer.data['id'])

    def create(self, request, *args, **kwargs):
        serializer = TripSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['creator_id'] = self.request.user.id
        serializer.validated_data['organisation_id'] = self.request.user.organisation.id
        serializer.validated_data['id'] = request.data['id']
        serializer.save()
        fse = FishServeEvents()
        fse.event_type = request.data['event_type']  # tripStart, trawl, etc.
        fse.json = request.data['json']
        fse.headers = request.data['headers']
        fse.creator = self.request.user
        fse.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        trip = self.get_object()
        trip.endTime = datetime.datetime.now()
        trip.save()
        fse = FishServeEvents()
        fse.event_type = request.data['event_type']  # tripStart, trawl, etc.
        fse.json = request.data['json']
        fse.headers = request.data['headers']
        fse.creator = self.request.user
        fse.save()
        return Response('trip updated')
