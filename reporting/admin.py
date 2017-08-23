from django.contrib import admin
from reporting.models import FishCatch, Species, Trip, Vessel, Port,\
    NonFishingEvent, FishingEvent, FishReciever, ProcessedState, Organisation


admin.site.register(Organisation)
admin.site.register(FishCatch)
admin.site.register(Species)
admin.site.register(Trip)
admin.site.register(Vessel)
admin.site.register(Port)
admin.site.register(NonFishingEvent)
admin.site.register(FishingEvent)
admin.site.register(FishReciever)
admin.site.register(ProcessedState)

from django.contrib.auth.admin import UserAdmin
from .models import User
admin.site.register(User, UserAdmin)
