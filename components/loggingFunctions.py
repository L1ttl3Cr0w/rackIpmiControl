import logging.config
import logging
import json

with open('logs_configs/log_config.json', 'r') as f:
    config = json.load(f)

logging.config.dictConfig(config)
def log_data(__name__,type, message):
    logger = logging.getLogger(__name__)
    if type == "critical":
        logger.critical(message)
    elif type == "error":
        logger.error(message)
    elif type == "warning":
        logger.warning(message)
    elif type == "info":
        logger.info(message)
    elif type == "debug":
        logger.debug(message)
    else:
            return logger.critical("log_data function has failed")