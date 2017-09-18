import os
import django
from base64 import b64encode
import json
import logging
from django.conf import settings
import time
from enum import Enum
from django.utils import timezone
from fishserve.models import FishServeEvents
from ecdsa.keys import SigningKey
import ecdsa
import requests
from django.core.management.base import BaseCommand
import hashlib


class Status(Enum):
    OK = "ok"
    ERROR = "error"


key = """-----BEGIN EC PARAMETERS-----
BggqhkjOPQMBBw==
-----END EC PARAMETERS-----
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIPAt+9XAGOPbCyPydiTt3u/9+1wG6RQp0Xm5Pgc5w/zRoAoGCCqGSM49
AwEHoUQDQgAEkzl+OeTttHQnc20ZYcd5AnULk1CK3InmiRgfIE7vDXlaYdcIcE5L
/TWBZQli/DgZfE6qEBzv22NpJRa4Gas/XA==
-----END EC PRIVATE KEY-----"""


installation_id = "5b3a58e2-2291-4acc-9fda-9197f5299190"


def register():
    login = {
      "username": "boddyr",
      "password": "Logisticsf1"
    }
    response = requests.post('https://api.uat.kupe.fishserve.co.nz/authenticate',
                             data=login)
    print("%s: %s" % (response.status_code, response.text))

    user_token = json.loads(response.text)['userToken']

    pubkey = """MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEkzl+OeTttHQnc20ZYcd5AnULk1CK3InmiRgfIE7vDXlaYdcIcE5L/TWBZQli/DgZfE6qEBzv22NpJRa4Gas/XA=="""
    reg = {
      "SoftwareVendor": "Fishery Logistics",
      "DeviceName": "Vessel Computer",
      "SoftwareInstallationId": installation_id,
      "PublicKey": pubkey
    }
    response = requests.post('https://ers.uat.kupe.fishserve.co.nz/api/security/log-book-registration',
                             data=reg,
                             headers={"Authorization": "Bearer " + user_token})
    print("%s: %s" % (response.status_code, response.text))


if __name__ == "__main__":
    #register()

    body = """{ "eventHeader":
{ "eventId": "aa58aca0-99c4-11e7-b6c4-6fd681ce18ab",
   "tripId": "aa58aca0-99c4-11e7-b6c4-6fd681ce18a0",
   "completedDateTime": "2017-09-18T15:12:30+12:00",
   "vesselNumber": "1",
   "isVesselUsed": true,
   "notes": "Some notes.",
   "softwareVendor": "Fishery Logistics",
   "softwareVersion": "1.0.0.0",
   "softwareInstallationId": "%s",
   "clientNumber": "9900159",
   "completerUserId": "9050" },
"personInCharge": "Rick Burch",
"startLocation":
 { "systemDateTime": "2017-09-18T15:12:30+12:00",
   "systemLocation": { "longitude": "-175.5423", "latitude": "-45.9880" },
   "manualDateTime": null,
   "manualLocation": null } }""" % installation_id

#    send_event("9900159", "event/v1/trip-start", 'aa58aca0-99c4-11e7-b6c4-6fd681ce18ab', {}, body.encode("utf-8"))


class Command(BaseCommand):
    help = 'Runs the fishserve integration daemon'
    log = logging.getLogger(__name__)

    def handle(self, *args, **options):
        self.log.warn("Starting FishServe integration daemon...")
        while True:
            self.send_pending_records()
            time.sleep(settings.FISHSERVE_SEND_INTERVAL)

    def send_pending_records(self):
        for fse in FishServeEvents.objects.filter(status__isnull=True).order_by('id').all():
            self.log.debug(fse)
            json_data = json.loads(fse.json)
            client_number = json_data['eventHeader']['clientNumber']
            event_id = json_data['eventHeader']['eventId']

            response = self.send_event(client_number, fse.event_type, event_id, fse.headers, fse.json)

            fse.processed = timezone.now()
            fse.response = "%s:%s" % (response.status_code, response.body)
            fse.status = Status.OK if response.status_code == 200 else Status.ERROR
            fse.save()

    def sign(self, payload, key):
        sk = SigningKey.from_pem(key, hashfunc=hashlib.sha256)
        signature = sk.sign(payload, sigencode=ecdsa.util.sigencode_der)
        return b64encode(signature)

    def send_event(self, client_number, event_type, event_id, headers, json):
        headers.update({'Content-Type': 'application/json',
                        'Content-Encoding': 'utf-8',
                        'Accept': 'application/json',
                        'Signature': self.sign(json, key)})
        self.log.debug(headers)
        params = {'clientNumber': client_number, 'eventId': event_id}
        response = requests.post('https://ers.uat.kupe.fishserve.co.nz/api/{clientNumber}/event/v1/trip-start/{eventId}'.format(**params),
                                 data=json,
                                 headers=headers)
        self.log.debug("%s: %s", response.status_code, response.text)
        return response
