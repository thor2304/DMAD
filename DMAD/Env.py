from decouple import config

root_logger_level: str = config("ROOT_LOGGER_LEVEL", default="DEBUG")

