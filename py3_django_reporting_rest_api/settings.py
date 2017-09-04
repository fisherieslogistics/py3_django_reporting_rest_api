from py3_django_reporting_rest_api.settings_common import *

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'fluent_fmt': {
            '()': 'fluent.handler.FluentRecordFormatter',
            'format': {
                'level': '%(levelname)s',
                'where': '%(module)s.%(funcName)s:%(lineno)s',
                'message': '%(msg)s',
                'stack_trace': '%(exc_text)s'
            }
        }
    },
    'handlers': {
        'fluentd': {
            'level': 'DEBUG',
            'class': 'fluent.handler.FluentHandler',
            'host': 'localhost',
            'port': 24224,
            'tag': 'test.logging',
            'formatter': 'fluent_fmt',
            'level': 'DEBUG',
        },
       'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['fluentd', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
