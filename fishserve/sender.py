import logging
from django.conf import settings
from django.db import transaction
import time
from enum import Enum
from django.utils import timezone
from simple_rest_client.api import API
from fishserve.models import FishServeEvents

log = logging.getLogger(__name__)


class Status(Enum):
    OK = "ok"
    ERROR = "error"


def sign(payload, keys):
    return "" # TODO


def get_api(clientNumber):
    api = API(
        api_root_url='https://ers.uat.kupe.fishserve.co.nz/api/%s/' % clientNumber,
        params={},
        headers={},
        timeout=30,
        append_slash=False,
        json_encode_body=True,
    )
    api.add_resource(resource_name='trawl', api_root_url="event/v1/trawl/")


def send_pending_records():
    for fse in FishServeEvents.objects.filter(status__isnull=True).order_by(id).all():
        log.debug(fse)
        api = get_api("TODO")
        response = api.trawl.create(body=fse.json, params={}, headers={})
        # TODO client number in the api url
        if response.status_code == 200:
            fse.status = Status.OK
            fse.processed = timezone.now()
            fse.response = ""  # TODO
            fse.save()
        else:
            # TODO


if __name__ == "__main__":
    while True:
        send_pending_records()
        time.sleep(settings.FISHSERVE_SEND_INTERVAL)
