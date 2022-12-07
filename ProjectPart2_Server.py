# Student Names:    Idil Bil & Suhail Khalil

import socket
import random
import time

HOST = "127.0.0.1"  #specified local host
PORT = 12000        #specified port
BUFFER = 4096       #maximum amount of data to be received at once 

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as serverSocket: #use with to create the server socket to simplify resource management
    serverSocket.bind((HOST, PORT))                                    #binds the socket to local port number 12000 and the loopback IP address
    
    while True:                                                       #creates an infinite loop so the server is always ready to recieve messages
        clientMessage, clientAddress = serverSocket.recvfrom(BUFFER)  #recieves message and the address from UDP socket, data received has to be smaller than the buffer
        
        received = clientMessage.decode().split()   #decodes the byte object into a string and seperates the string at every space
        i = received[1]                             #defines i as the second element in the message string as we expect a message of a specific format (and we never expect i to go higher than 9)

        print(clientMessage.decode())                       #prints clients message
        serverMessage = str("PING " + str(i) + " - ditto")  #modifies the message coming from client

        time.sleep(random.uniform(0.005,0.050))              #simulates the variability of the Round Trip Time within 5 to 50ms by waiting before responding
        ignore = random.random()                             #randomly generates a number between 0 and 1

        #simulates packet loss by only replying if random number is greater than 0.1 (with a 90% probability)
        if ignore > 0.1:
            serverSocket.sendto(serverMessage.encode(), clientAddress)  #sends back the modified message to the client
            
