from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from reporting.models import FishCatch, FishingEvent, Species, Trip, Vessel
import json
# Create your views here.
@csrf_exempt
def fishingEventWithCatches(request):
    print(request.body)
    fishingEventDict = json.loads(request.body.decode('utf-8'))
    print(fishingEventDict)
    trip = Trip.objects.get(RAId=fishingEventDict['tripRAId'])
    fishingEvent = FishingEvent()
    fishingEvent.locationAtEnd = fishingEventDict['locationAtEnd']
    fishingEvent.locationAtStart = fishingEventDict['locationAtStart']
    fishingEvent.datetimeAtStart = fishingEventDict['datetimeAtStart']
    fishingEvent.datetimeAtEnd = fishingEventDict['datetimeAtEnd']
    fishingEvent.eventSpecificDetails = fishingEventDict['eventSpecificDetails']
    fishingEvent.numberInTrip = fishingEventDict['numberInTrip']
    fishingEvent.vesselNumber = fishingEventDict['vesselNumber']
    fishingEvent.trip = trip
    fishingEvent.committed = True
    fishingEvent.isVesselUsed = fishingEventDict['isVesselUsed']

    fishingEvent.save()

    fishCatches = []
    for fc in fishingEventDict['fishCatches']:
        species = Species.objects.filter(code=fc['code']).first()
        if not species:
            continue
        fishCatch = FishCatch()
        fishCatch.species = species
        fishCatch.weightKgs = fc['weight']
        fishCatch.fishingEvent = fishingEvent
        fishCatch.save()
        fishCatches.append({ 'code': fishCatch.species.code, 'id': fishCatch.id })


    data = {
        'yee': 'haa',
        'id': fishingEvent.id
    }
    return JsonResponse(data)
