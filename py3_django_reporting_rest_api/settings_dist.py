from py3_django_reporting_rest_api.settings_common import *

SECRET_KEY = '+ec=dq4fm(yt0*x^9z0qw$-64ln_z83yjem#m#f4aG1fei5ZsA'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# TODO - why?
ALLOWED_HOSTS = ['*']

DATABASES = {
  'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': 'reporting',
      'USER': 'reportingadmin',
      'PASSWORD': 'nomorediscriminationagainstwhitepeopleindunedin',
      'HOST': 'fllpostgres',
      'PORT': '',
  }
}

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
        'django': {
            'handlers': ['syslog', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
