from pymongo import MongoClient
from dotenv import load_dotenv
from components.loggingFunctions import log_data
import os
# Loading default data variables for mongodb data registration
load_dotenv()
# server address written in .env
client = MongoClient(os.getenv("server"))
# the database that you will be accessing
db = client[os.getenv("database")]
# 
collection = db[os.getenv("collection")]
class db_template:
    def __init__(self, name, level, message):
        self.id = 1
        self.level = level
        self.message = message
        self.component = name.replace(".", "_")
    def update_logs(self):
        try:
            call = collection.find_one({"_id": 1})
            if call == None:
                collection.insert_one({"_id": self.id, f"{self.level}": [{f"{self.component}": f"{self.message}"}]})
            else:
                update_id = {"_id":self.id}
                post = {
                    "$push": {
                        f"{self.level}": {f"{self.component}":f"{self.message}"}
                    }
                }
                collection.update_one(update_id, post)
        except Exception as e:
            log_data(__name__, "error", f"Mongo database error: {e}")
        else:
            log_data(__name__, "info", "Logging data into mongodb was successfull")
def uploadData (level, message, name):
    db_template(1, level, message, name).update_logs()