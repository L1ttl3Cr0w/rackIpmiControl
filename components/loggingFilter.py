import logging
class FilterDebug(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelname == logging.getLevelName(logging.DEBUG)
class FilterInfo(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelname == logging.getLevelName(logging.INFO)
class FilterWarning(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelname == logging.getLevelName(logging.WARNING)
class FilterError(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelname == logging.getLevelName(logging.ERROR)
class FilterCritical(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelname == logging.getLevelName(logging.CRITICAL)
#class MyFilter(object):
#    def __init__(self, level):
#        self.__level = level
#    def filter(self, LogRecord):
#        return LogRecord.levelno == self.__level