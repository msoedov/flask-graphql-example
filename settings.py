import logging.config as log_config


class DevConfig(object):
    DEBUG = True

    SECRET_KEY = 'sdfsdf82347$$%$%$%$&fsdfs!!ASx+__WEBB$'

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
