from py3_django_reporting_rest_api.settings import *

PRESTASHOP_POLL_PERIOD = 60

DATABASES = {
  'default': {
      'ENGINE': 'django.contrib.gis.db.backends.postgis',
      'NAME': 'reporting',
      'USER': 'reportingadmin',
      'PASSWORD': 'nomorediscriminationagainstwhitepeopleindunedin',
      'HOST': 'localhost',
      'PORT': '',
      #'AUTOCOMMIT': False
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
