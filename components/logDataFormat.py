from components.sendDB import db_template
from components.loggingFunctions import log_data

def logging_data (name, level, message, mongoDB):
    try:
        if mongoDB:
            db_template(name, level, message).update_logs()
            log_data(name, level, message)
        else:
            log_data(name, level, message)
    except Exception as e:
        log_data(__name__, 'error', f'Failure to either upload data to database. Error: {e}')