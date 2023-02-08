import logging
import sys

import Env


s_info_formatter = {
    "format": "%(asctime)s: %(message)s",
    "datefmt": "%H:%M:%S"
}

stream_info_handler = {
    "class": "logging.StreamHandler",
    "level": "INFO",
    "formatter": "s_info_formatter",
    "stream": sys.stdout,
    'filters': ['allow_exactly_info'],
}

streamFormatter = {
    # "format": "%(message)s",
    "format": "%(asctime)s: %(levelname)-8s _ %(name)s _ : %(message)s",
    "datefmt": "%H:%M:%S",
    "class": "logging.Formatter"
}

streamHandler = {
    "class": "logging.StreamHandler",
    "level": "DEBUG",
    "formatter": "streamFormatter",
    "stream": sys.stdout,
    'filters': ['remove_externals'],
    # 'filters': ['exclude_info', 'remove_externals'],
}

#################
# loggers
root_handlers = ["streamHandler"]

root_logger = {
    "level": Env.root_logger_level,
    "handlers": root_handlers
}

info_handlers = ["stream_info_handler"]

info_logger = {
    "qualname": "info",
    "propagate": 1,
    "level": "INFO",
    "handlers": info_handlers,
}


###########
# filtering
class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level: int = logging.NOTSET):
        self.level = max_level

    def filter(self, record):
        if self.level == logging.NOTSET:
            allow = True
        else:
            allow = self.level >= record.levelno
        if not allow:
            print(f"filtered: {record.msg}")
        return allow


class ExactLevelFilter(logging.Filter):
    def __init__(self, exact_level: int = logging.NOTSET):
        self.level = exact_level

    def filter(self, record):
        if self.level == logging.NOTSET:
            print("logging filter set without level")
            allow = False
        else:
            allow = self.level == record.levelno
        if not allow:
            print(f"filtered: {record.msg}")
        return allow


class ApartFromRangeFilter(logging.Filter):
    def __init__(self, bottom_of_range: int = logging.NOTSET, top_of_range: int = logging.NOTSET):
        self.bottom_of_range = bottom_of_range
        self.top_of_range = top_of_range

    def filter(self, record):
        allow = record.levelno < self.bottom_of_range or record.levelno > self.top_of_range

        return allow


class RemoveExternalLogMessages(logging.Filter):
    def __init__(self):
        pass

    def filter(self, record):
        if record.name.startswith("websockets"):
            return False
        if record.name.startswith("urllib3"):
            return False
        return True


#############
# Framework setup

config_dict = {
    "version": 1,
    "loggers": {
        "info": info_logger,
    },
    "formatters": {
        "streamFormatter": streamFormatter,
        "s_info_formatter": s_info_formatter,
    },
    "filters": {
        "up_to_info": {
            '()': MaxLevelFilter,
            'max_level': logging.INFO,
        },
        "up_to_debug": {
            '()': MaxLevelFilter,
            'max_level': logging.DEBUG,
        },
        "allow_exactly_info": {
            '()': ExactLevelFilter,
            'exact_level': logging.INFO,
        },
        "exclude_info": {
            '()': ApartFromRangeFilter,
            'bottom_of_range': logging.INFO,
            'top_of_range': logging.INFO,
        },
        "remove_externals": {
            '()': RemoveExternalLogMessages,
        }
    },
    "handlers": {
        "streamHandler": streamHandler,
        "stream_info_handler": stream_info_handler
    },
    "root": root_logger
}
