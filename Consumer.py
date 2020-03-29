#Written by Alastair Lewis
#Consumes messages on localhost and dumps into a file
import os
import socket
from Database import Database

class Consumer:
    path = ""
    port = -1
    database = None

    #Instantiate with path to output file and port to listen on
    #Needs to be an Absolute Path to get proper saving functionality
    def __init__(self, path, port, database):
        self.path = path
        self.port = port
        self.database = database

    #Call this function once and it will continuously process messages
    def consume(self):
        message = ""
        #Setting up Socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', self.port))

        while True:
            #Waiting for connection
            s.listen(10)
            print("Waiting for a connection...")
            connection, client_address = s.accept()

            #Accepting connection
            print('Connection Accepted from: ' + str(client_address[0]))
            message = connection.recv(1024).decode()
            print("Recieved message: " + message)

            #Send to Database
            Database.writeRecord(message)

            #Write to file
            with open(self.path, 'a') as f:
                f.write(message + "\n")

            print("Message saved")
            message = ""

#Needs to be an Absolute Path to get proper saving functionality
d = Database("/Users/mackenziefurlong/Documents/CISC 498/Capstone")
c = Consumer("/Users/mackenziefurlong/Documents/CISC 498/Capstone/test.txt", 6969, d)
c.consume()
