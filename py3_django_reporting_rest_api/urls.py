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
    NonFishingEvent, FishingEvent, FishReciever, ProcessedState
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework.urlpatterns import format_suffix_patterns
from reporting import views
from reporting.serializers import TripViewSet, SpeciesViewSet, PortViewSet, NonFishEventViewSet,\
    VesselViewSet, ProcessedStateViewSet, FishCatchViewSet, FishingEventViewSet, FishRecieverViewSet

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"fishCatches", FishCatchViewSet)
router.register(r"fishingEvents", FishingEventViewSet)
router.register(r"trips", TripViewSet)
router.register(r"ports", PortViewSet)
router.register(r"vessels", VesselViewSet)
router.register(r"species", SpeciesViewSet)
router.register(r"nonfishprotecteds", NonFishEventViewSet)
router.register(r"processedStates", ProcessedStateViewSet)
router.register(r"species", SpeciesViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^admin/", admin.site.urls),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
]
