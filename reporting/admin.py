from django.contrib import admin
from reporting.models import FishCatch, Species, Trip, Vessel, Port,\
    NonFishProtectedSpeciesInteractionEvent, FishingEvent, FishReciever, ProcessedState


admin.site.register(FishCatch)
admin.site.register(Species)
admin.site.register(Trip)
admin.site.register(Vessel)
admin.site.register(Port)
admin.site.register(NonFishProtectedSpeciesInteractionEvent)
admin.site.register(FishingEvent)
admin.site.register(FishReciever)
admin.site.register(ProcessedState)
# Register your models here.
