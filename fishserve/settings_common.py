from py3_django_reporting_rest_api.settings import *
import os

FISHSERVE_SEND_INTERVAL = 10

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'fishserve',
]

TIME_ZONE = 'UTC'
USE_TZ = True

SECRET_KEY = '$t-)y+jm1vve443-orh$5!528p=b**y@#_4xts6g6^b!m$xr31'
