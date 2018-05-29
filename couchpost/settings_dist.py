from py3_django_reporting_rest_api.settings import *

COUCHDB_LISTENER_RETRY_TIMEOUT = 10
POSTGRES_POLL_PERIOD = 20
DOCUMENT_IMPORTER_POLL_PERIOD = 20

DATABASES = {
  'default': {
      'ENGINE': 'django.contrib.gis.db.backends.postgis',
      'NAME': 'reporting',
      'USER': 'reportingadmin',
      'PASSWORD': 'nomorediscriminationagainstwhitepeopleindunedin',
      'HOST': 'fllpostgres',
      'PORT': '',
      #'AUTOCOMMIT': False
  },
  'couchdb': {
      'USER': 'replicator',
      'PASSWORD': 'fishplicator',
      'URL': 'http://couchdb:5984/',
  }
}

import logging
logging.raiseExceptions = False # don't fail when syslog is not available

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'syslog_fmt': {'format': "%(asctime)s %(levelname)-5.5s [%(process)d:%(threadName)s][%(name)s.%(module)s.%(funcName)s:%(lineno)d] %(message)s"}
    },
    'handlers': {
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local0',
            'address': '/dev/log',
            'formatter': 'syslog_fmt',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'syslog'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
