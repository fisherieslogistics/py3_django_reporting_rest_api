from rest_framework import serializers, filters
from reporting.models import Trip, FishingEvent, Species, FishCatch, NonFishingEvent, \
    Port, ProcessedState, Vessel, Organisation, User, LandingEvent
from fishserve.models import FishServeEvents


class FishServeEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = FishServeEvents
        fields = (
            "event_type",
            "json",
            "headers",
            "status",
            "creator"
        )
