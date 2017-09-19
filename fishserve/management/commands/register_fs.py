from base64 import b64encode
import json
import logging
from django.conf import settings
from ecdsa.keys import SigningKey
import requests
from django.core.management.base import BaseCommand
import hashlib
from reporting.models import User
import uuid
from ecdsa import curves


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

        response = requests.post(settings.FISHSERVE_AUTH_URL, data=login)
        self.log.debug("%s: %s", response.status_code, response.text)
        user_token = json.loads(response.text)['userToken']

        # generate new keys and installation stuff
        priv_key = SigningKey.generate(curve=curves.NIST256p, hashfunc=hashlib.sha256)
        pub_key = priv_key.get_verifying_key()
        installation_id = str(uuid.uuid4())

        reg = {"SoftwareVendor": "Fishery Logistics",
               "DeviceName": "Vessel iPad",
               "SoftwareInstallationId": installation_id,
               "PublicKey": b64encode(pub_key.to_der()).decode('ascii')}
        self.log.debug(reg)

        response = requests.post(settings.FISHSERVE_API_URL + '/security/log-book-registration',
                                 data=reg,
                                 headers={"Authorization": "Bearer " + user_token})
        self.log.debug("%s: %s", response.status_code, response.text)

        u.update_extra_info({'fishserve': {'installationId': installation_id, 'private_key': b64encode(priv_key.to_der()).decode('ascii'), 'public_key': b64encode(pub_key.to_der()).decode('ascii')}})
        u.save()

        self.log.info("Registration successfull. Installation_id: %s", installation_id)
