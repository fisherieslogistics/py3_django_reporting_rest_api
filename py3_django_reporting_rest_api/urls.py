"""py3_django_reporting_rest_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r"^$", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r"^$", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r"^blog/", include("blog.urls"))
""",
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import User
from reporting.models import FishCatch, Species, Trip, Vessel, Port,\
    NonFishProtectedSpeciesInteractionEvent, FishingEvent, FishReciever, ProcessedState
from rest_framework import serializers, viewsets, routers


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


class NonFishProtectedSpeciesInteractionEventSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = NonFishProtectedSpeciesInteractionEvent
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


class NonFishProtectedSpeciesInteractionEventViewSet(viewsets.ModelViewSet):
    queryset = NonFishProtectedSpeciesInteractionEvent.objects.all()
    serializer_class = NonFishProtectedSpeciesInteractionEventSerializer


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



# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"fishCatches", FishCatchViewSet)
router.register(r"fishingEvents", FishingEventViewSet)
router.register(r"trips", TripViewSet)
router.register(r"ports", PortViewSet)
router.register(r"vessels", VesselViewSet)
router.register(r"species", SpeciesViewSet)
router.register(r"nonfishprotecteds", NonFishProtectedSpeciesInteractionEventViewSet)
router.register(r"processedStates", ProcessedStateViewSet)
router.register(r"species", SpeciesViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^admin/", admin.site.urls),
]
