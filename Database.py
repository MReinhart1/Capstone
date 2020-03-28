
from app import app
import json

class Database:
    path = ""
    def __init__(self, path):
        self.path = path
    def writeRecord(self, record):
        record = json.loads(record)
        machine = record["machine"]
        time = record["time"]
        userID = record["userID"]
        print(machine)
        print(time)
        print(userID)
        app.insertUsageRecord()
        
