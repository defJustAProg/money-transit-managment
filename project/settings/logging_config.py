import os

from project.django.settings import BASE_DIR, DEBUG

if DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[%(asctime)s] [%(levelname)s] %(module)s : %(message)s",
                "datefmt": "%d.%m.%Y %H:%M:%S",
            },
            "message_only": {"format": "%(message)s"},
        },
        "handlers": {
            "django_file": {
                "level": "DEBUG",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "verbose",
                "filename": os.path.join(BASE_DIR, "logs/webserver.log"),
                "backupCount": 7,
                "when": "midnight",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["django_file"],
                "level": "DEBUG",
                "propagate": True,
            },
            "django.request": {
                "handlers": ["django_file"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }
