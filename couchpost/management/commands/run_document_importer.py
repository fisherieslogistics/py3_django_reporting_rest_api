import logging
from django.conf import settings
import time
from django.core.management.base import BaseCommand
from couchpost.document_importer import CouchDBDocumentImporter


class Command(BaseCommand):
    help = 'Runs the document importer service'
    log = logging.getLogger(__name__)

    def handle(self, *args, **options):
        self.log.info("Starting document importer daemon...")

        while True:
            try:
                CouchDBDocumentImporter().poll_pending_documents()
            except:
                self.log.exception("Integration service failed.")

            time.sleep(settings.DOCUMENT_IMPORTER_POLL_PERIOD)
