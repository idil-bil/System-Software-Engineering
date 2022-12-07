# Group#:           G2
# Student Names:    Idil Bil & Suhail Khalil
# student numbers:  21344189 - 56517816

import socket
import time

HOST = "127.0.0.1"  #specified local host
PORT = 12000        #specified port
BUFFER = 4096       #maximum amount of data to be received at once 

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as clientSocket:   #use with to create the client socket to simplify resource management
    i = 1

    while i <= 5:                                                     #need to send the message 5 times
        clientMessage = str("PING " + str(i) + " - hello world")      #creates client message

        clientSocket.sendto(clientMessage.encode(),(HOST, PORT))      #sends the message to the server by encoding the string into a bytes object
        sendTime = time.time()                                        #records the time the message was sent in seconds
        clientSocket.settimeout(1)                                    #use the settimeout method to set the timeout at 1 sec
        
        #Use try except to attempt to receive and decode the server's response and calculate RTT
        #If a timeout exception is raised then we print "request timed out" and move on
        try:
            serverMessage, serverAddress = clientSocket.recvfrom(BUFFER)  #attemps to recieve the response from the server
            print(serverMessage.decode())                                 #decodes the serverMessage from a bytes object to a string and prints it
            i += 1
            recieveTime = time.time()                                     #records the time the message was recieved in seconds
            delay = (recieveTime - sendTime)*1000                         #calculates the response delay in milliseconds
            print(f"RTT = {delay:9.4f}ms")
        except socket.timeout:
            print("Request timed out")
            i += 1
        

       
