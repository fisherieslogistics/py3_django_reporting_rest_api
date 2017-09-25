import logging
from django.conf import settings
from couchpost.models import PendingDocument
import time
from enum import Enum

log = logging.getLogger(__name__)


class Status(Enum):
    OK = "ok"
    ERROR = "error"
    EXCEPTION = "exception"


class TripProcessor():
    pass


class FisningEventProcessor():
    pass


class NonFishingEventProcessor():
    pass


class FishCatchProcessor():
    pass


class VesselLocationProcessor():
    pass


class FishServeEventProcessor():
    #def process(self, doc):
    #    FishServeEvents()
    pass


class DocumentType(Enum):
    trip = TripProcessor()
    fishingEvent = TripProcessor()
    fishingCatch = FishCatchProcessor()
    nonFishingEvent = TripProcessor()
    vesselLocation = VesselLocationProcessor()
    fishserveEvent = TripProcessor()


class CouchDBDocumentImporter():

    def error(self, pending_doc, message, status=Status.ERROR):
        pending_doc.process_status = status
        pending_doc.details = message
        pending_doc.save()

    def process_document(self, pd):
        if not pd.doc:
            self.error(pd, "Document is empty.")
        try:
            processor = getattr(DocumentType, pd.doc['document_type']).value
        except (AttributeError, TypeError):
            self.error("Unknown document type: %s" % pd.doc.get('document_type', "None"))

        return processor.process(pd.doc)

    def poll_pending_documents(self):
        for pd in PendingDocument.objects.filter(process_status__isnull=True).order_by('id').all():
            model = self.process_document(pd)
            model.save()
