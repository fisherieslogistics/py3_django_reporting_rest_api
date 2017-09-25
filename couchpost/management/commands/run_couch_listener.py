import logging
from django.conf import settings
import time
from django.core.management.base import BaseCommand
from couchpost.couch_listener import listen_for_couch_changes


class Command(BaseCommand):
    help = 'Runs the couchdb listener replication service'
    log = logging.getLogger(__name__)

    def handle(self, *args, **options):
        self.log.info("Starting couchdb listener daemon...")

        while True:
            try:
                listen_for_couch_changes()
            except:
                self.log.exception("Integration service failed.")

            time.sleep(settings.COUCHDB_LISTENER_RETRY_TIMEOUT)
