from py3_django_reporting_rest_api.settings_common import *

SECRET_KEY = '+ec=dq4fm(yt0*x^9z0qw$-64ln_z83yjem#m#f4z36*cnk8ve'

DEBUG = True

DATABASES = {
  'default': {
      'ENGINE': 'django.contrib.gis.db.backends.postgis',
      'NAME': 'reporting',
      'USER': 'reportingadmin',
      'PASSWORD': 'nomorediscriminationagainstwhitepeopleindunedin',
      'HOST': 'fllpostgres',
      'PORT': '',
      'ATOMIC_REQUESTS': True
  },
  'couchdb': {
      'USER': 'replicator',
      'PASSWORD': 'fishplicator',
      'URL': 'http://couchdb:5984/',
  }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'console_fmt': {'format': "%(asctime)s %(levelname)-5.5s [%(threadName)s][%(name)s.%(module)s.%(funcName)s:%(lineno)d] %(message)s"}
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'console_fmt',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
