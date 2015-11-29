import logging.config as log_config
import os

from mongoengine import connect


class DevConfig(object):
    DEBUG = True if os.getenv('DEBUG', default='') else False

    SECRET_KEY = 'sdfsdf82347$$%$%$%$&fsdfs!!ASx+__WEBB$'

    MONGODB_IP = os.getenv('DB_PORT_27017_TCP_ADDR', '127.0.0.1')
    MONGODB_SETTINGS = {
        'db': 'tumblelog',
        'host': MONGODB_IP,
        'port': 27017
    }
    connect(**MONGODB_SETTINGS)
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {

        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'null': {
                'level': 'ERROR',
                'class': 'logging.NullHandler',
            },

        },
        'loggers': {
            'flask': {
                'handlers': ['console'],
                'propagate': False,
            },
            'factory': {
                'handlers': ['null'],
                'level': 'ERROR',
                'propagate': False,
            },

            'app': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
            '': {
                'handlers': ['null'],
                'level': 'ERROR',
                'propagate': False,
            },
        }
    }
    log_config.dictConfig(LOGGING)
    import coloredlogs
    coloredlogs.install()
