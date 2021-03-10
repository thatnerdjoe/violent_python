'''
Simple Client Data Transfer in the clear

In this example a connection is made between a client
and simple server running on the same machine over a 
pre-defined and agreed upon port.

This client application will transfer a simple text message
to the server.  The server will will simply display the contents  
of the message.

'''
from __future__ import print_function

import socket           # Import Python Standard Socket Library
import sys

print("Client Application")
print("Establish a connection to a server")
print("Available on the same host using PORT 5555")

PORT = 5555          # Port Number of Server
    
try:
    # Create a Socket
    clientSocket = socket.socket()
    
    # Get my local host address
    localHost = socket.gethostname()
    
    print("\nAttempt Connection to: ", localHost, PORT)
    
    clientSocket.connect((localHost, PORT))
    
    # Sending message if there was a connection
    print("Socket Connected ...")
    print("Sending Message to Server")
    clientSocket.sendall(b'Hello Universe')
    
except Exception as err:
    sys.exit(err)

            
