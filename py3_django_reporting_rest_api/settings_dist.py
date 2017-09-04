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
        'fluent_fmt': {
            '()': 'fluent.handler.FluentRecordFormatter',
            'format': {
                'level': '%(levelname)s',
                #'hostname': '%(hostname)s',
                'where': '%(module)s.%(funcName)s:%(lineno)s',
                'message': '%(msg)s',
                'stack_trace': '%(exc_text)s'
            }
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/debug.log',
        },
        'fluentd': {
            'level': 'DEBUG',
            'class': 'fluent.handler.FluentHandler',
            'host': 'fluentd',
            'port': 24224,
            'tag': 'test.logging',
            'formatter': 'fluent_fmt',
            'level': 'DEBUG'
        }
   },
    'loggers': {
        'django': {
            'handlers': ['fluentd', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
