import datetime

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, \
    ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from fishserve.models import FishServeEvents
from reporting.models import Organisation, Trip, FishingEvent, FishCatch, \
    ProcessedState, Vessel, NonFishingEvent, Port, Species, User
from reporting.serializers import OrganisationSerializer, MyUserMixIn, \
    MyOrganisationMixIn, TripSerializer, TripExpandSerializer, \
    LandingEventSerializer, TripSubmitSerializer, FishingEventExpandSerializer, \
    FishingEventSubmitSerializer, ProcessedStateSerializer, VesselSerializer, \
    NonFishEventSerializer, PortSerializer, SpeciesSerializer, UserSerializer


class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer


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

    def partial_update(self, request, pk=None):
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


class FishingEventViewSet(MyUserMixIn, CreateModelMixin, GenericViewSet):

    queryset = FishingEvent.objects.all()
    serializer_class = FishingEventExpandSerializer

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


class ProcessedStateViewSet(viewsets.ModelViewSet):
    queryset = ProcessedState.objects.all()
    serializer_class = ProcessedStateSerializer


class VesselViewSet(MyOrganisationMixIn, viewsets.ModelViewSet):
    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer


class NonFishEventViewSet(viewsets.ModelViewSet):
    queryset = NonFishingEvent.objects.all()
    serializer_class = NonFishEventSerializer


class PortViewSet(MyOrganisationMixIn, viewsets.ModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PortSerializer


class SpeciesViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


class UserViewSet(MyOrganisationMixIn, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


