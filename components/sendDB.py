from pymongo import MongoClient
from dotenv import load_dotenv
from components.loggingFunctions import log_data
import os
import datetime
# Loading default data variables for mongodb data registration
load_dotenv()
# server address written in .env
client = MongoClient(os.getenv("server"))
# the database that you will be accessing
db = client[os.getenv("database")]
# collection that the data will be going to
collection = db[os.getenv("collection")]
class db_template:
    def __init__(self, name, level, message):
        self.id = 2
        self.level = level
        self.message = message
        self.component = name.replace(".", "_")
        self.current_time = datetime.datetime.now()
    def update_logs(self):
        try:
            call = collection.find_one({"_id": self.id})
            if call == None:
                collection.insert_one({"_id": self.id, self.current_time.strftime("%Y_%m_%d"):{self.current_time.strftime("hour_%H"):{self.level:[{"component":self.component, "message":self.message, "time":self.current_time.strftime("%M-%S")}]}}})
            else:
                update_id = {"_id":self.id}
                post = {
                    "$push": {
                        f"{self.current_time.strftime("%Y_%m_%d")}.{self.current_time.strftime("hour_%H")}.{self.level}":{"component":self.component, "message":self.message, "time":self.current_time.strftime("%M-%S")}
                    }
                }
                collection.update_one(update_id, post)
        except Exception as e:
            log_data(__name__, "error", f"Mongo database error: {e}")
        else:
            log_data(__name__, "info", "Logging data into mongodb was successfull")
def uploadData (level, message, name):
    db_template(level, message, name).update_logs()