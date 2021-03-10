# Python Packet Capture Script
# Python Script to record IP and OS Observations
# Running on Linux or Windows
# Import Standard Library Modules


import argparse         # Python Standard Library - Parser for command-line options, arguments
import socket           # network interface library used for raw sockets
import signal           # generation of interrupt signals i.e. timeout
import os               # operating system functions i.e. file I/o
from struct import *    # Handle Strings as Binary Data 
import datetime         # Python Standard Library date and time methods
import time             # Python Standard Library time methods
import pickle           # Python Standard Library pickle methods
import platform         # Python Standard Library platform
import sys              # Python Standard Library System Module

# CONSTANTS

PROTOCOL_TCP = 6
PROTOCOL_UDP = 17

#
# Name: ValDirWrite
#
# Desc: Function that will validate a directory path as 
#       existing and writable.  Used for argument validation only
#
# Input: a directory path string
#  
# Actions: 
#              if valid will return the Directory String
#
#              if invalid it will raise an ArgumentTypeError within argparse
#              which will inturn be reported by argparse to the user
#

def ValDirWrite(theDir):

    # Validate the path is a directory
    if not os.path.isdir(theDir):
        raise argparse.ArgumentTypeError('Directory does not exist')

    # Validate the path is writable
    if os.access(theDir, os.W_OK):
        return theDir
    else:
        raise argparse.ArgumentTypeError('Directory is not writable')

#End ValDirWrite ===================================


# Create timeout class to handle capture duration

class myTimeout(Exception):
    pass

# Create a signal handler that raises a timeout event
# when the capture duration is reached

def handler(signum, frame):
    if VERBOSE:
        print ('Capture Complete', signum)
        print()
        
    raise myTimeout()

#  
# Class: IPObservationDictionary
#
# Desc: Handles all methods and properties
#       relating to the IPOservations 
#
#

class IPObservationDictionary:

    # Constructor
    
    def __init__(self):
        
        #Attributes of the Object
        
        self.Dictionary = {}            # Dictionary to Hold IP Observations
   
    # Method to Add an observation
    
    def AddOb(self, key):
       
        # Obtain the current hour
        
        now = datetime.datetime.now()
        hour = now.hour

        # Check to see if key is already in the dictionary
        
        if key in self.Dictionary:
        
            # If yes, retrieve the current value
            curValue = self.Dictionary[key]
            
            # Increment the count for the current hour
            curValue[hour-1] = curValue[hour-1] + 1
            
            # Update the value associated with this key
            self.Dictionary[key] = curValue
        
        else:
            # if the key doesn't yet exist
            # Create one
            
            curValue = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            
            # Increment the count for the current hour
            curValue[hour-1] = curValue[hour-1] + 1
    
            self.Dictionary[key] = curValue

    # Method to retrieve an observation
    # If no observation found return None
    
    def GetOb(self,key):
        
        if key in self.Dictionary:
            curValue = self.Dictionary[key]
            return curValue
        else:
            return None
        
    # Print the Contents of the Dictionary
    
    def PrintOb(self):
        print ("\nIP Observations")
        print ("Unique Combinations:    ", str(len(self.Dictionary)))
        print()
        
        # Print Heading

        print ("                                                |-------------------------------------------  Hourly Observations --------------------------------------------------|")
        print()
        
        print ('%16s' % "Server", end=" ")
        print ('%16s' % "Client", end=" ")
        print ('%7s'  % "Port",   end=" ")
        print ('%5s'  % "Type",   end=" ")
        
        for i in range(0, 24):
            print  (' ', end=" ")           
            print ('%02d' % i,end=" ")
        print()
        
        # Print Contents
        for keys,values in self.Dictionary.items():        
            
            print ('%16s' % keys[0],end=" ")
            print ('%16s' % keys[1],end=" ")
            print ('%7s'  % str(keys[2]),end=" ")
            print ('%5s'  % keys[3],end=" ")
            
            for i in range(0, 24):
                print ('%4s' % str(values[i]),end=" ")
            print()
            
    # Save the Current Observation Dictionary
    # to the specified file
    
    def SaveOb(self, fileName):
        
        with open(fileName, 'wb') as fp:
            pickle.dump(self.Dictionary, fp)             
        
    # Load in and Observation Dictionary
    # from the specified file
    
    def LoadOb(self, fileName):
        
        with open(fileName, 'rb') as fp:
            self.Dictionary = pickle.loads(fp.read())
        
    # Destructor Delete the Object
    
    def __del__(self):
        if VERBOSE:
            print ("Closed")
        
# End IPObservationClass ====================================


#  
# Class: OSObservationDictionary
#
# Desc: Handles all methods and properties
#       relating to the IPOservations 
#
#

class OSObservationDictionary:

    # Constructor
    
    def __init__(self):
        
        #Attributes of the Object
        
        self.Dictionary = {}            # Dictionary to Hold IP Observations
   
    # Method to Add an observation
    
    def AddOb(self, key):
       
        # Obtain the current hour
        
        now = datetime.datetime.now()
        hour = now.hour

        # Check to see if key is already in the dictionary
        
        if key in self.Dictionary:
        
            # If yes, retrieve the current value
            curValue = self.Dictionary[key]
            
            # Increment the count for the current hour
            curValue[hour-1] = curValue[hour-1] + 1
            
            # Update the value associated with this key
            self.Dictionary[key] = curValue
        
        else:
            # if the key doesn't yet exist
            # Create one
            
            curValue = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            
            # Increment the count for the current hour
            curValue[hour-1] = curValue[hour-1] + 1
    
            self.Dictionary[key] = curValue

    # Method to retrieve an observation
    # If no observation found return None
    
    def GetOb(self,key):
        
        if key in self.Dictionary:
            curValue = self.Dictionary[key]
            return curValue
        else:
            return None

    # Print the Contents of the Dictionary
    
    def PrintOb(self):
        
        print ("\nOS Observations")
        print ("Unique Combinations:    ", str(len(self.Dictionary)))        
        
        # Print Heading
        print ("                                |-------------------------------------------  Hourly Observations  --------------------------------------------------|")
        print()
        print ('%16s' % "Server",end=" ")
        print ('%7s'  % "Port",end=" ")
        print ('%5s'  % "Type",end=" ")
        
        for i in range(0, 24):
            print (' ',  end=" ")          
            print ('%02d' % i,end=" ")
        print()
        
           # Print Contents
        for keys,values in self.Dictionary.items():
            print ('%16s' % keys[0],end=" ")
            print ('%7s'  % str(keys[2]),end=" ")
            print ('%5s'  % keys[3],end=" ")
            
            for i in range(0, 24):
                print ('%4s' % str(values[i]),end=" ")
            print()
          
    # Save the Current Observation Dictionary
    # to the specified file
    
    def SaveOb(self, fileName):
        
        with open(fileName, 'wb') as fp:
            pickle.dump(self.Dictionary, fp)             
        
    # Load in and Observation Dictionary
    # from the specified file
    
    def LoadOb(self, fileName):
        
        with open(fileName, 'rb') as fp:
            self.Dictionary = pickle.loads(fp.read())
        
    # Destructor Delete the Object
    
    def __del__(self):
        if VERBOSE:
            print ("Closed")
        
# End IPObservationClass ====================================



# PacketExtractor
#
# Purpose: Extracts fields from the IP and TCP Header
#
# Input:   packet:     buffer from socket.recvfrom() method
# Output:  list:       serverIP, clientIP, serverPort
#

def PacketExtractor(packet):
    
    if PLATFORM == "LINUX":
            
        ETH_LEN  = 14      # ETHERNET HDR LENGTH
        IP_LEN   = 20      # IP HEADER    LENGTH
        UDP_LEN  = 8       # UPD HEADER   LENGTH
        
    elif PLATFORM == "WINDOWS" or PLATFORM == "MAC":
        
        ETH_LEN  = 0       # ETHERNET HDR LENGTH
        IP_LEN   = 20      # IP HEADER    LENGTH
        UDP_LEN  = 8       # UPD HEADER   LENGTH        
    
    ethernetHeader=packet[0:IP_LEN]
        
    #Strip off the first 20 characters for the ip header
    ipHeader = packet[ETH_LEN:ETH_LEN+IP_LEN]
     
    #now unpack them
    ipHeaderTuple = unpack('!BBHHHBBH4s4s' , ipHeader)
        
    # unpack returns a tuple, for illustration I will extract
    # each individual values
                                           # Field Contents
    verLen       = ipHeaderTuple[0]        # Field 0: Version and Length
    TOS          = ipHeaderTuple[1]        # Field 1: Type of Service                                      
    packetLength = ipHeaderTuple[2]        # Field 2: Packet Length
    packetID     = ipHeaderTuple[3]        # Field 3: Identification  
    flagFrag     = ipHeaderTuple[4]        # Field 4: Flags and Fragment Offset
    RES          = (flagFrag >> 15) & 0x01 # Reserved
    DF           = (flagFrag >> 14) & 0x01 # Don't Fragment
    MF           = (flagFrag >> 13) & 0x01 # More Fragments
    timeToLive   = ipHeaderTuple[5]        # Field 5: Time to Live (TTL)
    protocol     = ipHeaderTuple[6]        # Field 6: Protocol Number 
    checkSum     = ipHeaderTuple[7]        # Field 7: Header Checksum
    sourceIP     = ipHeaderTuple[8]        # Field 8: Source IP
    destIP       = ipHeaderTuple[9]        # Field 9: Destination IP    
    
    # Calculate / Convert extracted values
    
    version      = verLen >> 4             # Upper Nibble is the version Number
    length       = verLen & 0x0F           # Lower Nibble represents the size
    ipHdrLength  = length * 4              # Calculate the header length in bytes
    
    # covert the source and destination address to typical dotted notation strings
       
    sourceAddress      = socket.inet_ntoa(sourceIP);
    destinationAddress = socket.inet_ntoa(destIP);
    
    if protocol == PROTOCOL_TCP:
        
        stripTCPHeader = packet[ETH_LEN+ipHdrLength:ipHdrLength+ETH_LEN+IP_LEN]
             
        # unpack returns a tuple, for illustration I will extract
        # each individual values using the unpack() function

        tcpHeaderBuffer = unpack('!HHLLBBHHH' , stripTCPHeader)
         
        sourcePort             = tcpHeaderBuffer[0]
        destinationPort        = tcpHeaderBuffer[1]
        sequenceNumber         = tcpHeaderBuffer[2]
        acknowledgement        = tcpHeaderBuffer[3]
        dataOffsetandReserve   = tcpHeaderBuffer[4]
        tcpHeaderLength        = (dataOffsetandReserve >> 4) * 4
        flags                  = tcpHeaderBuffer[5]
        FIN                    = flags & 0x01
        SYN                    = (flags >> 1) & 0x01
        RST                    = (flags >> 2) & 0x01
        PSH                    = (flags >> 3) & 0x01
        ACK                    = (flags >> 4) & 0x01
        URG                    = (flags >> 5) & 0x01
        ECE                    = (flags >> 6) & 0x01
        CWR                    = (flags >> 7) & 0x01
        windowSize             = tcpHeaderBuffer[6]
        tcpChecksum            = tcpHeaderBuffer[7]
        urgentPointer          = tcpHeaderBuffer[8]
        
        if sourcePort <= 1024:              # Assume server IP is server
            serverIP   = sourceAddress
            clientIP   = destinationAddress
            serverPort = sourcePort
            status = True
        elif destinationPort <= 1024:       # Assume destination IP is server
            serverIP   = destinationAddress
            clientIP   = sourceAddress
            serverPort = destinationPort
            status = True
        elif sourcePort <= destinationPort: # Assume server IP is server
            serverIP   = sourceAddress
            clientIP   = destinationAddress
            serverPort = sourcePort
            status = True
        elif sourcePort > destinationPort:  # Assume distinatin IP is server
            serverIP   = destinationAddress
            clientIP   = sourceAddress
            serverPort = destinationPort
            status = True         
        else:                               # Should never get here
            serverIP   = "FILTER"
            clientIP   = "FILTER"
            serverPort = "FILTER"
            status = False
        
        return( status, (serverIP, clientIP, serverPort, "TCP"), [SYN, serverIP, TOS, timeToLive, DF, windowSize] )
    
    elif protocol == PROTOCOL_UDP:
        
        stripUDPHeader = packet[ETH_LEN+ipHdrLength:ETH_LEN+ipHdrLength+UDP_LEN]
             
        # unpack returns a tuple, for illustration I will extract
        # each individual values using the unpack() function

        udpHeaderBuffer = unpack('!HHHH' , stripUDPHeader)
         
        sourcePort             = udpHeaderBuffer[0]
        destinationPort        = udpHeaderBuffer[1]
        udpLength              = udpHeaderBuffer[2]
        udpChecksum            = udpHeaderBuffer[3]

        if sourcePort <= 1024:              # Assume server IP is server
            serverIP   = sourceAddress
            clientIP   = destinationAddress
            serverPort = sourcePort
            status = True
        elif destinationPort <= 1024:       # Assume destination IP is server
            serverIP   = destinationAddress
            clientIP   = sourceAddress
            serverPort = destinationPort
            status = True
        elif sourcePort <= destinationPort: # Assume server IP is server
            serverIP   = sourceAddress
            clientIP   = destinationAddress
            serverPort = sourcePort
            status = True
        elif sourcePort > destinationPort:  # Assume distinatin IP is server
            serverIP   = destinationAddress
            clientIP   = sourceAddress
            serverPort = destinationPort
            status = True         
        else:                               # Should never get here
            serverIP   = "FILTER"
            clientIP   = "FILTER"
            serverPort = "FILTER"
            status = False
        
        return( status, (serverIP, clientIP, serverPort, "UDP"), ["FILTER","FILTER","FILTER","FILTER","FILTER","FILTER"] )
        
    else:
        
        return( False, ("Filter", "Filter", "Filter", "FILTER"), ["FILTER","FILTER","FILTER","FILTER","FILTER","FILTER"] )


# 
# Class Spinner
#
# Used to display a spinning character on the screen to show progress
#
#

class Spinner:
    
    # Constructor
    
    def __init__(self):
    
        print("Packet Observations")
        self.dotCnt = 0
         
    def Spin(self):
        
        if self.dotCnt > 40:
            print()
            self.dotCnt = 0
        else:
            sys.stdout.write('.')        
            sys.stdout.flush()
            self.dotCnt += 1 

# End Spinner Class


# Main Program Starts Here
#===================================

if __name__ == '__main__':

    # Setup Argument Parser Object

    parser = argparse.ArgumentParser('P2NMAP-Capture')
       
    parser.add_argument('-v', '--verbose', help="Display packet details", action='store_true')
    parser.add_argument('-m',  '--minutes', help='Capture Duration in minutes',type=int)  
    parser.add_argument('-p',  '--outPath', type= ValDirWrite, required=True, help="Output Directory")         
    
    theArgs = parser.parse_args()    
    
    VERBOSE = theArgs.verbose

    # Calculate capture duration
    captureDuration = theArgs.minutes * 60
        
    try:
        # Note script must be run in superuser mode
        # i.e. sudo python ..
        
        if platform.system() == "Linux":
            
            PLATFORM = "LINUX"
            
            # Enable Promiscous Mode on the NIC
            # Make a system call 
            # Note: Linux Based
            
            ret =  os.system("ifconfig eth0 promisc")
            if ret != 0:
                print ('Promiscious Mode not Set')
                quit()                
            
            # create a new socket using the python socket module
            # PF_PACKET   : Specifies Protocol Family Packet Level
            # SOCK_RAW    : Specifies A raw protocol at the network layer
            # socket.htons(0x0800) : Specifies all headers and packets
            #                      : Ethernet and IP, including TCP/UDP etc
            
            # Attempt to open the socket for capturing raw packets
    
            rawSocket=socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0800))
    
            # Set the signal handler to the duraton specified by the user
            
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(captureDuration)
                
        elif platform.system() == "Windows":
            
            PLATFORM = "WINDOWS"
            
            # For the Windows Platform the setup is also different
            
            # Retreive our our IP Address to bind to
            hostname = socket.gethostname()
            host = socket.gethostbyname(hostname)
            
            # Create a rawSocket
            rawSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
            # Set the socket Options
            rawSocket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            # Bind to our host
            rawSocket.bind( (host,0))
            # Set socket to receive all packets
            rawSocket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)  
            
            startTime = time.time()
            endTime = startTime + captureDuration
            
        else:
            print ("Platform not supported")
            quit()
    except Exception as err:
        print ("Socket Error", err)
        quit()
        
    if VERBOSE:
        print ("Network      : Promiscous Mode")
        print ("Sniffer      : Ready: \n")
        
        # Create a Spinner Object for displaying progress
        obSPIN = Spinner()  

    # Create IP and OS observation dictionaires
    
    ipOB = IPObservationDictionary() 
    osOB = OSObservationDictionary()
        
    # Create a perpetual loop, we will be 
    # interrupted by the timeout value only    
    
    packetsCaptured = 0
    try: 
        while True:
            
            # attempt to recieve (this call is synchronous, thus it will wait)
            receivedPacket=rawSocket.recv(65535)
            
            packetsCaptured += 1            # Count the captured packets
            
            if VERBOSE:
                # Update the Display
                obSPIN.Spin()
            
            # decode the received packet
            # call the local packet extract function above
            
            status, osContent, fingerPrint = PacketExtractor(receivedPacket)
            
            # If status returns true
            # we can process the results
            
            if status:
                
                # Add content to ipObservations
                
                ipOB.AddOb(osContent)
                    
                if fingerPrint[0] == 1:
                    osContent = tuple(fingerPrint[1:])
                    osOB.AddOb(osContent)

            else:
                # Not a valid packet
                continue
            
            if PLATFORM == "WINDOWS":
                if time.time() > endTime:
                    raise myTimeout

    except myTimeout:
        pass
    
    # Capture Complete
    
    if VERBOSE:
                    
        print ("\nTotal Packets Captured: ", str(packetsCaptured))
        print()
        
        ipOB.PrintOb()
        osOB.PrintOb()        
        
        print ("\nSaving Observations ext: .ipDict and .osDict")
    
    ipOutFile = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".ipDict"
    osOutFile = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".osDict"
    
    ipOutput = os.path.join(theArgs.outPath, ipOutFile)
    osOutput = os.path.join(theArgs.outPath, osOutFile)
    
    ipOB.SaveOb(ipOutput)
    osOB.SaveOb(osOutput)           
    
    if PLATFORM == "LINUX":
        # Disable Promiscous Mode on the NIC
        # Make a system call 
        # Note: Linux Based
     
        ret =  os.system("ifconfig eth0 -promisc")
                
    elif PLATFORM == "WINDOWS":
        rawSocket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
          
    else:
        print ("Platform not supported")
        quit()
    
    # Close the Raw Socket
    rawSocket.close()

    
