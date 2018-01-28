import logging
from couchpost.models import PendingDocument
from enum import Enum
from fishserve.models import FishServeEvents
from reporting.models import Trip, FishingEvent, NonFishingEvent, FishCatch,\
    VesselLocation, Vessel
from django.db import transaction
from django.utils import timezone
from reporting.serializers import TripSerializer, FishingEventExpandSerializer,\
    FishCatchSerializer, NonFishEventSerializer
from fishserve.serializers import FishServeEventSerializer


class Status(Enum):
    OK = "ok"
    ERROR = "error"
    EXCEPTION = "exception"


class ValidationError(RuntimeError):
    pass


class DocumentFactory():

    """ returns instance with given fields, but removes extraneous fields - Dnajgo would fail otherwise """
    @classmethod
    def _cleanInstance(cls, model_cls, data):
        # TODO this is a bit retarded and there must be a better way to do this...
        fields = set([v.name for v in model_cls._meta.get_fields(True, True)] + [v.attname if hasattr(v, 'attname') else v.name for v in model_cls._meta.get_fields(True, True)])
        for k in set(data.keys()).difference(fields):
            del data[k]

        return model_cls(**data)

    @classmethod
    def trip(cls, pd):
        # TODO implement update
        organisation_id = pd.doc['organisation_id']
        if organisation_id != str(pd.user.organisation_id):
            raise ValidationError("Organisation ID's don't match: %s != %s" % (organisation_id, pd.user.organisation_id))
        return cls._cleanInstance(Trip, {**{'creator': pd.user}, **pd.doc})

    @classmethod
    def fishingEvent(cls, pd):
        # TODO implement update
        trip = Trip.objects.get(pk=pd.doc['trip_id'])
        if trip.organisation_id != pd.user.organisation_id:
            raise ValidationError("Organisation ID's don't match: %s != %s" % (trip.organisation_id, pd.user.organisation_id))
        return cls._cleanInstance(FishingEvent, {**{'creator': pd.user}, **pd.doc})

    @classmethod
    def fishCatch(cls, pd):
        event = FishingEvent.objects.get(pk=pd.doc['fishingEvent_id'])
        trip = event.trip
        if trip.organisation_id != pd.user.organisation_id:
            raise ValidationError("Organisation ID's don't match: %s != %s" % (trip.organisation_id, pd.user.organisation_id))
        return cls._cleanInstance(FishCatch, pd.doc)

    @classmethod
    def nonFishingEvent(cls, pd):
        trip = Trip.objects.get(pk=pd.doc['trip_id'])
        if trip.organisation_id != pd.user.organisation_id:
            raise ValidationError("Organisation ID's don't match: %s != %s" % (trip.organisation_id, pd.user.organisation_id))
        return cls._cleanInstance(NonFishingEvent, pd.doc)

    @classmethod
    def vesselLocation(cls, pd):
        vessel = Vessel.objects.get(pk=pd.doc['vessel_id'])
        if vessel.organisation_id != pd.user.organisation_id:
            raise ValidationError("Organisation ID's don't match: %s != %s" % (vessel.organisation_id, pd.user.organisation_id))
        return cls._cleanInstance(VesselLocation, pd.doc)

    @classmethod
    def fishserveEvent(cls, pd):
        return cls._cleanInstance(FishServeEvents, {**{'creator_id': pd.user.id}, **pd.doc})


class CouchDBDocumentImporter():
    def error(self, pending_doc, message, status):
        logging.error("Document ID %s cannot be processed: %s", pending_doc.id, message)
        pending_doc.process_status = status.value
        pending_doc.details = message
        pending_doc.processed = timezone.now()
        pending_doc.save()

    def process_document(self, pd):
        try:
            if not pd.doc:
                raise ValidationError("Document is empty.")

            if 'document_type' not in pd.doc:
                raise ValidationError("Missing document_type.")

            try:
                factory = getattr(DocumentFactory, pd.doc['document_type'])
            except (AttributeError):
                raise ValidationError("Unknown document type: %s" % pd.doc.get('document_type', "None"))

            del pd.doc["document_type"]

            model = factory(pd)
            with transaction.atomic():
                model.save()
                pd.process_status = Status.OK.value
                pd.processed = timezone.now()
                pd.save()

            return model
        except ValidationError as e:
            logging.error("Error processing document %s: %s", pd.id, e.__repr__())
            self.error(pd, e.__repr__(), Status.ERROR)
        except Exception as e:
            logging.exception("Error processing document %s", pd.id)
            self.error(pd, e.__repr__(), Status.EXCEPTION)

    def poll_pending_documents(self):
        for pd in PendingDocument.objects.filter(process_status__isnull=True).order_by('id').all():
            self.process_document(pd)
