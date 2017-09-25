import logging
from django.conf import settings
import time
from django.core.management.base import BaseCommand
from couchpost.post_poller import poll_postgres_for_changes


class Command(BaseCommand):
    help = 'Runs the postgres poller replication service'
    log = logging.getLogger(__name__)

    def handle(self, *args, **options):
        self.log.info("Starting postgres poller daemon...")

        while True:
            try:
                poll_postgres_for_changes()
            except:
                self.log.exception("Integration service failed.")

            time.sleep(settings.POSTGRES_POLL_PERIOD)
