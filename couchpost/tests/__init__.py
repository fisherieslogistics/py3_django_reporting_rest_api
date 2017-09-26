import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "py3_django_reporting_rest_api.settings")

django.setup(set_prefix=False)
