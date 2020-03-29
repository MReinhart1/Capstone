#Stub Class for Database written by: Alastair Lewis
#Michael Reinhart needs to update this file with any Database code that he needs
import app
import json
class Database:
    path = ""

    def __init__(self, path):
        self.path = path

    def writeRecord(record):
        record = json.loads(record)
        machine = record["machine"]
        time = record["time"]
        userID = record["userID"]
        app.writeUsageRecord(machine, time, userID)
        app.machineStatus(machine)
