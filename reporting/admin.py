from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reporting.models import FishCatch, Species, Trip, Vessel, Port,\
    NonFishingEvent, FishingEvent, ProcessedState, Organisation, User


class MyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {'fields': (
            'organisation',
            'username',
            'email',
            'extra_info',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, { 'fields': (
            'organisation',
            'extra_info',
        )}),
    )


admin.site.register(Organisation)
admin.site.register(FishCatch)
admin.site.register(Species)
admin.site.register(Trip)
admin.site.register(Vessel)
admin.site.register(Port)
admin.site.register(NonFishingEvent)
admin.site.register(FishingEvent)
admin.site.register(ProcessedState)
admin.site.register(User)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
