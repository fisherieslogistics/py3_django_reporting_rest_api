from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from models import FishCatch, FishingEvent, Species
# Create your views here.
@csrf_exempt
def fishingEventWithCatches(request):

    print("have reqyested data")
    print(request)
    print(request)
    data = {
        'yee': 'haa',
    }
    return JsonResponse(data)
