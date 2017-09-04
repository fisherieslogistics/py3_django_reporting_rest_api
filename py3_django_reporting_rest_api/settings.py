from py3_django_reporting_rest_api.settings_common import *

DEBUG = True

SECRET_KEY = '+ec=dq4fm(yt0*x^9z0qw$-64ln_z83yjem#m#f4z36*cnk7ve'

DATABASES = {
  'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': 'reporting',
      'USER': 'reportingadmin',
      'PASSWORD': 'nomorediscriminationagainstwhitepeopleindunedin',
      'HOST': 'localhost',
      'PORT': '',
  }
}
