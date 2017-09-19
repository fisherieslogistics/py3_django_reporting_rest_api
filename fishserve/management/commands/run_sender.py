from base64 import b64encode, b64decode
import json
import logging
from django.conf import settings
import time
from enum import Enum
from fishserve.models import FishServeEvents
from ecdsa.keys import SigningKey
import ecdsa
import requests
from django.core.management.base import BaseCommand
import hashlib
from django.utils import timezone


class Status(Enum):
    OK = "ok"
    ERROR = "error"


class Command(BaseCommand):
    help = 'Runs the fishserve integration daemon'
    log = logging.getLogger(__name__)

    def handle(self, *args, **options):
        self.log.info("Starting FishServe integration daemon...")

        while True:
            self.send_pending_records()
            time.sleep(settings.FISHSERVE_SEND_INTERVAL)

    def send_pending_records(self):
        self.log.debug("Checking for new events...")
        for fse in FishServeEvents.objects.filter(status__isnull=True).order_by('id').all():
            self.log.debug(fse)
            json_data = json.loads(fse.json)
            client_number = json_data['eventHeader']['clientNumber']
            event_id = json_data['eventHeader']['eventId']

            response = self.send_event(client_number, fse.event_type, event_id, fse.headers, fse.json.encode('utf-8'), fse.creator)

            fse.processed = timezone.now()
            fse.response = "%s:%s" % (response.status_code, response.text)
            fse.status = Status.OK.value if response.status_code in [200, 201] else Status.ERROR.value
            fse.save()

    def sign(self, payload, key):
        sk = SigningKey.from_der(b64decode(key), hashfunc=hashlib.sha256)
        signature = sk.sign(payload, sigencode=ecdsa.util.sigencode_der)
        return b64encode(signature)

    def send_event(self, client_number, event_type, event_id, headers, json, creator):
        headers = dict(headers)  # create a copy so we don't modify the database record
        headers.update({'Content-Type': 'application/json',
                        'Content-Encoding': 'utf-8',
                        'Accept': 'application/json',
                        'Signature': self.sign(json, creator.extra_info['fishserve']['private_key'])})
        self.log.debug(headers)

        params = {'clientNumber': client_number, 'event_type': event_type, 'eventId': event_id}

        response = requests.post(settings.FISHSERVE_API_URL + '/{clientNumber}/event/{event_type}/{eventId}'.format(**params),
                                 data=json,
                                 headers=headers)

        self.log.debug("%s: %s", response.status_code, response.text)

        return response
