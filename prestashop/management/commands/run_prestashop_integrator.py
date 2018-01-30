import logging
from django.conf import settings
import time
from django.core.management.base import BaseCommand
from prestashop.prestashop_integrator import PrestashopIntegrator


class Command(BaseCommand):
    help = 'Runs the prestashop integration service'
    log = logging.getLogger(__name__)

    def handle(self, *args, **options):
        self.log.info("Starting prestashop integration daemon...")

        while True:
            try:
                PrestashopIntegrator().update_stock()
            except:
                self.log.exception("Integration service failed.")

            time.sleep(settings.PRESTASHOP_POLL_PERIOD)
