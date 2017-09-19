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
from reporting.models import User
from ecdsa.curves import SECP256k1
import uuid
from fishserve.management.commands.run_sender import installation_id


class Command(BaseCommand):
    help = 'Creates installation ID in Fishserve'
    log = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)
        parser.add_argument('fishserve_username', nargs='+', type=str)
        parser.add_argument('fishserve_password', nargs='+', type=str)

        parser.add_argument(
            '--client',
            action='store',
            dest='client',
            help='Sets client number on the organisation',
        )

    def handle(self, *args, **options):
        self.log.debug(args)
        self.log.debug(options)
        u = User.objects.get(username=options['username'][0])
        self.log.debug(u)

        # update org if needed
        if ("client" in options):
            u.organisation.update_extra_info({'fishserve': {'clientNumber': options['client']}})
            u.organisation.save()

        # login and get token
        login = {"username": options['fishserve_username'][0],
                 "password": options['fishserve_password'][0]}

        response = requests.post('https://api.uat.kupe.fishserve.co.nz/authenticate', data=login)
        self.log.debug("%s: %s", response.status_code, response.text)
        user_token = json.loads(response.text)['userToken']

        # generate new keys and installation stuff
        priv_key = SigningKey.generate(curve=SECP256k1, hashfunc=hashlib.sha256)
        pub_key = priv_key.get_verifying_key()
        installation_id = str(uuid.uuid4())

        reg = {"SoftwareVendor": "Fishery Logistics",
               "DeviceName": "Vessel iPad",
               "SoftwareInstallationId": installation_id,
               "PublicKey": b64encode(pub_key.to_der())}

        response = requests.post('https://ers.uat.kupe.fishserve.co.nz/api/security/log-book-registration',
                                 data=reg,
                                 headers={"Authorization": "Bearer " + user_token})
        self.log.debug("%s: %s", response.status_code, response.text)

        u.update_extra_info({'fishserve': {'installationId': installation_id, 'private_key': str(priv_key.to_pem()), 'public_key': str(pub_key.to_pem())}})
        u.save()

        self.log.info("Registration successfull. Installation_id: %s", installation_id)
