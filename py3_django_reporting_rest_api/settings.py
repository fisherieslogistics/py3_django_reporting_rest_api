from py3_django_reporting_rest_api.settings_common import *

DEBUG = True

SECRET_KEY = '+ec=dq4fm(yt0*x^9z0qw$-64ln_z83yjem#m#f4z36*cnk7ve'

DATABASES = {
  'default': {
      'ENGINE': 'django.contrib.gis.db.backends.postgis',
      'NAME': 'reporting',
      'USER': 'reportingadmin',
      'PASSWORD': 'nomorediscriminationagainstwhitepeopleindunedin',
      'HOST': 'localhost',
      'PORT': '',
  }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
       'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
