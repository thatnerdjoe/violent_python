'''

Copyright (c) 2017- 2020 Python Forensics and Chet Hosmer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

Revision History

SPECIAL NOTE:  This script is experimental

v .99-1 Experimental Release  (October 2020)

Written exclusively for Python 3.4.x or above

Overview:

The script ingests a standard PCAP File and creates a passive
asset map based on the observed UNIQUE activity and stores the
resultng map as a serialzed python object.  In addition, an html
file is generated that depicts the observed asset map.


'''
# Python Standard Library Module Imports

import tkinter.font as tkfont
from tkinter import Tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import *  # TK GUI Components
from pcapfile.protocols.transport import udp
from pcapfile.protocols.transport import tcp
from pcapfile.protocols.network import ip
from pcapfile.protocols.linklayer import ethernet
from pcapfile import savefile
import re
import sys               # System specifics
import platform          # Platform specifics
import os                # Operating/Filesystem Module
import time              # Basic Time Module
import logging           # Script Logging
import time              # Time Functions
import hashlib           # Hashing module
import pickle            # Object Serialization
import webbrowser        # Webbrowser
import collections       # Python collections library
from binascii import unhexlify
from HTMLReport import HTML_START, HTML_SECTION, HTML_ENTRY, HTML_PORTS, HTML_ENTRY_PORTS, HTML_TABLE_END, HTML_END
from collections import OrderedDict

'''

Simple PCAP File 3rd Party Library
to process pcap file contents

To install the Library
pip install pypcapfile

'''


'''
Python Core GUI Library
tkinter GUI Components from the Standard Library
'''

# Script Constants

NAME = "pfAssetMap"
VERSION = "Version .99 July 2020 Experimental"
AUTHOR = "C. Hosmer"
TITLE = NAME+'\t'+VERSION
DEBUG = True

# Script Constants

SYSTEM = platform.system()
PYTHON = sys.version[0:6]

LOG = "./PCAP_SCRIPT_LOG.txt"
OVERWRITE = True        # Overwrite the Log on Each execution

# Screen Colors
BG = 'white'
FG = 'black'


# Script Local Functions

'''
InitLog: Initialize the Forensic Log

'''


def InitLog():

    try:
        # If LOG should be overwritten before
        # each run, the remove the old log
        if OVERWRITE:
            # Verify that the log exists before removing
            if os.path.exists(LOG):
                os.remove(LOG)

        # Initialize the Log include the Level and message
        logging.basicConfig(
            filename=LOG, format='%(levelname)s\t:%(message)s', level=logging.DEBUG)

    except:
        quit()

# End of Forensic Log Initialization

# Function: LogEvent()
#
# Logs the event message and specified type
# Input:
#        eventMessage : string containing the message to be logged


def LogEvent(eventMessage):

    try:

        if type(eventMessage) == str:

            re.sub(r'[^\x00-\x7f]', r'', eventMessage)

            timeStr = GetTime('UTC')
            # Combine current Time with the eventMessage
            # You can specify either 'UTC' or 'LOCAL'
            # Based on the GetTime parameter

            eventMessage = str(timeStr)+": "+eventMessage
            logging.info(eventMessage)

    except:
        pass

# End LogEvent Function


# Function: GetTime()
#
# Returns a string containing the current time
#
# Script will use the local system clock, time, date and timezone
# to calcuate the current time.  Thus you should sync your system
# clock before using this script
#
# Input: timeStyle = 'UTC', 'LOCAL', the function will default to
#                    UTC Time if you pass in nothing.

def GetTime(timeStyle="UTC"):

    if timeStyle == 'UTC':
        return ('UTC Time:  ', time.asctime(time.gmtime(time.time())))
    elif timeStyle == 'LOCAL':
        return ('Local Time:', time.asctime(time.localtime(time.time())))
    else:
        return "Invalid TimeStyle Specified"

# End GetTime Function


class ETH:

    def __init__(self):

        self.ethTypes = {}

        self.ethTypes[2048] = "IPv4"
        self.ethTypes[2054] = "ARP"
        self.ethTypes[34525] = "IPv6"

    def lookup(self, ethType):

        try:
            result = self.ethTypes[ethType]
        except:
            result = "not-supported"

        return result

# MAC Address Lookup Class


class MAC:

    def __init__(self):

        # Open the MAC Address OUI Dictionary
        with open('oui.pickle', 'rb') as pickleFile:
            self.macDict = pickle.load(pickleFile)

    def lookup(self, macAddress):
        try:
            result = self.macDict[macAddress]
            return result
        except:
            return ["", "", ""]

# Transport Lookup Class


class TRANSPORT:

    def __init__(self):

        # Open the transport protocol Address OUI Dictionary
        with open('protocol.pickle', 'rb') as pickleFile:
            self.proDict = pickle.load(pickleFile)

    def lookup(self, protocol):
        try:
            result = self.proDict[protocol]
            return result
        except:
            return ["unknown", "unknown", "unknown"]

# PORTS Lookup Class


class PORTS:

    def __init__(self):

        # Open the MAC Address OUI Dictionary
        with open('ports.pickle', 'rb') as pickleFile:
            self.portDict = pickle.load(pickleFile)

    def lookup(self, port, portType):
        try:
            result = self.portDict[(port, portType)]
            return result
        except:
            return "EPH"


class IPObservationDictionary:

    # Constructor

    def __init__(self):

        # Attributes of the Object

        self.Dictionary = {}            # Dictionary to Hold IP Observations
        self.portObservations = {}

    # Method to Add an observation

    def AddOb(self, key, mac, hour):

        # Check to see if key is already in the dictionary

        if key in self.Dictionary:

            # If yes, retrieve the current value
            curValue = self.Dictionary[key]

            curMac = curValue[0]
            hours = curValue[1]

            # Increment the count for the current hour
            hours[hour-1] = hours[hour-1] + 1

            # Update the value associated with this key
            self.Dictionary[key] = [curMac, hours]

        else:
            # if the key doesn't yet exist
            # Create one

            curHours = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            # Increment the count for the current hour
            curHours[hour-1] = curHours[hour-1] + 1

            self.Dictionary[key] = [mac, curHours]

    def AddPortOb(self, key, desc):

        # Check to see if key is already in the dictionary

        if key not in self.portObservations:

            self.portObservations[key] = desc

    def CreateHTML(self, path, sTime, eTime, pkts, tFile, tOrg, tAnalyst, tBase):

        fldReportFile = os.path.join(
            path, (time.strftime("%Y-%m-%d-%H%M")+"-assetMap")+".html")

        hmtlContents = HTML_START
        htmlContents = hmtlContents+HTML_SECTION
        fldScriptName = "Python Network Asset Mapping Report"
        fldAuthor = "Joseph Miller"
        fldVersion = "Version 0.1"
        fldTarget = tFile
        fldAnalyst = tAnalyst
        fldOrg = tOrg
        fldBaseline = tBase
        fldStart = sTime
        fldEnd = eTime
        fldPkts = pkts
        fldSectionName = "Observations Histogram"

        htmlContents = htmlContents.format(**locals())
        self.Dictionary = OrderedDict(sorted(self.Dictionary.items()))
        for eachKey in self.Dictionary:
            htmlBody = HTML_ENTRY

            value = self.Dictionary[eachKey]

            fldSrcIP = '{:14s}'.format(eachKey[0])
            fldDstIP = '{:14s}'.format(eachKey[1])

            fldSrcPort = '{:4s}'.format(eachKey[2])
            fldDstPort = '{:4s}'.format(eachKey[3])
            fldType = '{:5s}'.format(eachKey[4])

            fldHr = []

            hourData = value[1]
            macData = value[0]

            fldSrcMAC = macData[0]
            fldDstMAC = macData[2]

            mfgCC = macData[1][0]
            mfgDesc = macData[1][1]
            fldSrcMFG = mfgCC+":"+mfgDesc[0:16]

            mfgCC = macData[3][0]
            mfgDesc = macData[3][1]
            fldDstMFG = mfgCC+":"+mfgDesc[0:16]

            for i in range(0, 24):
                fldHr.append('{: >5d}'.format(hourData[i]))

            htmlBody = htmlBody.format(**locals())
            htmlContents = htmlContents+htmlBody

        htmlContents = htmlContents + HTML_TABLE_END

        portList = []

        for key, value in self.portObservations.items():
            portList.append([key[0], key[1], value])

        portList.sort()
        lastServer = ""

        htmlPorts = HTML_PORTS

        for eachEntry in portList:
            htmlPortsEntry = HTML_ENTRY_PORTS

            if eachEntry[0] != lastServer:
                fldPortIP = ""
                fldPortNum = ""
                fldPortDesc = ""
                htmlPortsEntry = htmlPortsEntry.format(**locals())
                htmlPorts = htmlPorts + htmlPortsEntry

                htmlPortsEntry = HTML_ENTRY_PORTS
                fldPortIP = eachEntry[0]
                fldPortNum = eachEntry[1]
                fldPortDesc = eachEntry[2]
                lastServer = eachEntry[0]
                htmlPortsEntry = htmlPortsEntry.format(**locals())
                htmlPorts = htmlPorts + htmlPortsEntry

            else:
                fldPortIP = ""
                fldPortNum = eachEntry[1]
                fldPortDesc = eachEntry[2]
                htmlPortsEntry = htmlPortsEntry.format(**locals())
                htmlPorts = htmlPorts + htmlPortsEntry

        htmlPorts = htmlPorts + HTML_TABLE_END
        htmlContents = htmlContents + htmlPorts
        htmlContents = htmlContents + HTML_END

        # Output that file
        output = open(fldReportFile, "w")
        output.write(htmlContents)
        output.close()
        return fldReportFile

    # Save the Current Observation Dictionary
    # to the specified file

    def SaveOb(self, path):

        baseline = os.path.join(path, (time.strftime(
            "%Y-%m-%d-%H%M")+"-assetMap")+".baseline")

        with open(baseline, 'wb') as fp:
            pickle.dump(self.Dictionary, fp)

    # Destructor Delete the Object

    def __del__(self):
        pass

# End IPObservationClass ====================================


'''
APPLICATION CLASS GUI FRAME USING TKINKER

Establish the GUI Environment

'''


class Application(Frame):

    def __init__(self, master=None):

        # Define the instance variables to be
        # collected from the GUI

        self.targetPath = "./PCAP/"
        self.ReportFolder = "./REPORTS/"
        self.BaselinePath = "./BASELINES/"
        self.abortFlag = False

        # Create Lookup Objects
        self.macOBJ = MAC()
        self.traOBJ = TRANSPORT()
        self.portOBJ = PORTS()
        self.ethOBJ = ETH()

        # Create First Entry in the Log
        LogEvent("Start Search")
        LogEvent(TITLE)

        # Create the basic frame
        Frame.__init__(self, master)
        self.parent = master

        self.parent.resizable(0, 0)

        # Intialize the GUI
        self.initUI()

    '''
    Initialize the GUI components
    - Menu Bar
    - Root Folder Selection
    - Progress Bar
    - Perform Search Button
    - Status Bar
    '''

    def initUI(self):

        # Create Menu Bar
        menuBar = Menu(self.parent)  # menu begin
        toolsMenu = Menu(menuBar, tearoff=0)

        toolsMenu.add_command(
            label='About Search', accelerator='Ctrl+A', command=self.menuAbout, underline=0)

        toolsMenu.add_separator()

        toolsMenu.add_command(
            label='Exit', accelerator='Ctrl+X', command=self.menuToolsExit)

        menuBar.add_cascade(label='Help', menu=toolsMenu, underline=0)

        self.parent.config(menu=menuBar)  # menu ends

        self.bind_all("<Control-x>", self.menuToolsExit)
        self.bind_all("<Control-a>", self.menuAbout)

        # Case Specifics Investigator, Organization and Case
        self.investigatorValue = Label(
            self.parent, anchor='w', text="Analyst: ")
        self.investigatorValue.grid(
            row=0, column=0, padx=5, pady=5, sticky='w')

        self.nValue = StringVar()
        self.nValue = ''
        self.entryAnalyst = Entry(
            self.parent, textvariable=self.nValue, width=50)
        self.entryAnalyst.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.orgValue = Label(self.parent, anchor='w', text="Organization: ")
        self.orgValue.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.oValue = StringVar()
        self.oValue = ''
        self.entryOrganization = Entry(
            self.parent, textvariable=self.oValue, width=50)
        self.entryOrganization.grid(
            row=1, column=1, padx=5, pady=5, sticky='w')

        self.caseValue = Label(self.parent, anchor='w',
                               text="Baseline Description: ")
        self.caseValue.grid(row=2, column=0, padx=5, pady=5, sticky='w')

        self.bValue = StringVar()
        self.bValue = ''
        self.entryBaseline = Entry(
            self.parent, textvariable=self.bValue, width=50)
        self.entryBaseline.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # Target File to Search
        self.lblTarget = Label(self.parent, anchor='w', text="Target PCAP")
        self.lblTarget.grid(row=3, column=0, padx=5, pady=10, sticky='w')

        self.targetFile = Label(
            self.parent, anchor='w', bd=3, bg='white', fg='black', width=60, relief=SUNKEN)
        self.targetFile.grid(row=3, column=1, padx=5, pady=0, sticky='w')

        self.buttonTargetFile = Button(self.parent, text=' ... ', command=self.btnSelectFile,
                                       width=5, bg='gray', fg='white', activebackground='black', activeforeground='green')
        self.buttonTargetFile.grid(row=3, column=2, padx=5, pady=0, sticky='w')

        self.searchButton = Button(self.parent, text='Create Asset Map', command=self.btnCreateAssetMap,
                                   bg='gray', fg='white', activebackground='black', activeforeground='green')
        self.searchButton.grid(row=4, column=1, padx=5, pady=5, sticky=W)
        self.searchButton['state'] = DISABLED

        self.htmlButton = Button(self.parent, text='View Report', command=self.btnViewReport,
                                 width=10, bg='gray', fg='white', activebackground='black', activeforeground='green')
        self.htmlButton.grid(row=4, column=2, padx=5, pady=5, sticky='w')
        self.htmlButton['state'] = DISABLED

        # SETUP a Progress Bar

        self.progressLabel = Label(self.parent, anchor='w', text="Progress  %")
        self.progressLabel.grid(row=6, column=0, padx=5, pady=10, sticky='w')

        self.progressBar = ttk.Progressbar(self.parent, style="red.Horizontal.TProgressbar", orient="horizontal",
                                           length=0, mode="determinate")

        self.progressBar.grid(row=6, column=1, padx=5, pady=10, sticky='w')

        self.statusText = Label(
            self.parent, anchor='w', width=80, bd=3, bg='white', fg='black', relief=SUNKEN)
        self.statusText.grid(row=7, column=0, columnspan=3,
                             padx=5, pady=5, sticky='w')
        self.update()

        # Special Code to align the width of the progress bar

        colWidth = self.targetFile.winfo_width()
        self.progressBar['length'] = colWidth

        self.statusText['text'] = "Waiting..."

        self.update()

    '''
    ALL Button and EVENT HANDLERS
    Code Area
    '''

    # Handle Folder Browse Button Click

    def btnSelectFile(self):
        fileName = filedialog.askopenfilename(
            initialdir="./PCAP/",  title='Select a file to Search')
        self.targetFile['text'] = fileName
        self.targetPath = fileName

        if self.targetPath:
            self.searchButton['state'] = NORMAL
            self.update()
            self.statusText['text'] = "Target File Selected: "+self.targetPath
            LogEvent("Target File Selected: "+self.targetPath)

    # Handle Perform Search Button Click

    def btnCreateAssetMap(self):

        if self.targetFile:

            self.progressBar['value'] = 0
            self.statusText['text'] = "Processing PCAP ... Please Wait "
            self.update()

            # Create IP observation dictionary object
            self.ipOB = IPObservationDictionary()

            self.StartTime = GetTime()
            pcapFile = self.targetFile['text']
            try:
                icsCapture = open(pcapFile, 'rb')
                capture = savefile.load_savefile(
                    icsCapture, layers=0, verbose=False)
            except:
                # Unable to ingest pcap
                self.statusText['text'] = "!! Unsupported PCAP File Format !! "
                self.update()
                return

            startTime = GetTime()
            totPackets = 0
            currentProgress = 0
            pktCnt = 0

            self.update()

            # Count the total Number of packets (used for progress bar)
            for pkt in capture.packets:
                totPackets += 1

            # Now process each packet
            for pkt in capture.packets:
                pktCnt += 1

                # Get the raw ethernet frame
                ethFrame = ethernet.Ethernet(pkt.raw())

                '''
                Ethernet Header
                0                   1                   2                   3                   4
                0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                |                                      Destination Address                                      |
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                |                                         Source Address                                        |
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                |           EtherType           |                                                               |
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                                                               +
                |                                                                                               |
                +                                            Payload                                            +
                |                                                                                               |
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

                '''

                ''' ---- Extract the source mac address ---- '''
                srcMAC = "".join(map(chr, ethFrame.src))
                srcMAC = srcMAC[0:8].upper()
                # remove the colon seperators
                # note the variable names starting with fld, we will use these later
                fldSrcMAC = re.sub(':', '', srcMAC)

                # Attempt to lookup the mfg in our lookup table
                fldSrcMFG = self.macOBJ.lookup(fldSrcMAC)

                ''' Extract the destination mac address ---'''
                dstMAC = "".join(map(chr, ethFrame.dst))
                dstMAC = dstMAC[0:8].upper()
                # remove the colon seperators
                # note the variable names starting with fld, we will use these later
                fldDstMAC = re.sub(':', '', dstMAC)

                # Attempt to lookup the mfg in our lookup table
                fldDstMFG = self.macOBJ.lookup(fldDstMAC)

                ''' --- create a list of mac addresses and manufacture ouis '''
                macData = [fldSrcMAC, fldSrcMFG, fldDstMAC, fldDstMFG]

                ''' Lookup the Frame Type '''
                frameType = self.ethOBJ.lookup(ethFrame.type)

                ''' Process any IPv4 Frames '''

                if frameType == "IPv4":
                    '''
                    ipV4 Header
                    0                   1                   2                   3
                    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
                    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                    |Version|  IHL  |Type of Service|          Total Length         |
                    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                    |         Identification        |Flags|     Fragment Offset     |
                    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                    |  Time to Live |    Protocol   |        Header Checksum        |
                    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                    |                         Source Address                        |
                    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                    |                      Destination Address                      |
                    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                    |                    Options                    |    Padding    |
                    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                    '''

                    ''' Extract the payload '''
                    ipPacket = ip.IP(unhexlify(ethFrame.payload))

                    ''' Extra Credit
                        Obtain the Time to Live Value from the IP packet
                        hint ipPacket.ttl
                        Add the TTL field to the report, this will require
                        careful study of how the information is stored
                        using the self.ipOB.AddOb() method and you also need
                        to modify the HTMLReport.py and self.ipOB.CreateHTML() method
                        to match.
                    '''

                    ''' Extract the source and destination ip addresses '''
                    srcIP = "".join(map(chr, ipPacket.src))
                    dstIP = "".join(map(chr, ipPacket.dst))

                    ''' Extract the protocol in use '''
                    protocol = str(ipPacket.p)

                    ''' Lookup the transport protocol in use '''
                    transport = self.traOBJ.lookup(protocol)[0]

                    if transport == "TCP":

                        '''
                        TCP HEADER
                        0                   1                   2                   3
                        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
                        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                        |          Source Port          |        Destination Port       |
                        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                        |                        Sequence Number                        |
                        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                        |                     Acknowledgment Number                     |
                        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                        | Offset|  Res. |     Flags     |             Window            |
                        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                        |            Checksum           |         Urgent Pointer        |
                        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                        |                    Options                    |    Padding    |
                        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                        '''

                        tcpPacket = tcp.TCP(unhexlify(ipPacket.payload))

                        srcPort = tcpPacket.src_port
                        dstPort = tcpPacket.dst_port

                        # Lookup Port Description, if not found assume Ephemeral
                        srcPortDesc = self.portOBJ.lookup(str(srcPort), "TCP")
                        if srcPortDesc == "EPH":
                            srcPort = "EPH"
                        else:
                            srcPort = str(srcPort)

                        dstPortDesc = self.portOBJ.lookup(str(dstPort), "TCP")
                        if dstPortDesc == "EPH":
                            dstPort = "EPH"
                        else:
                            dstPort = str(dstPort)

                        timeStruct = time.gmtime(pkt.timestamp)

                        # extract the hour the packet was captured
                        theHour = timeStruct.tm_hour

                        # Add a new IP observation and the hour
                        self.ipOB.AddOb(
                            (srcIP, dstIP, srcPort, dstPort, "TCP"), macData, theHour)

                        # Post them to PortObject Dictionary
                        if srcPort != "EPH":
                            self.ipOB.AddPortOb((srcIP, srcPort), srcPortDesc)
                        if dstPort != "EPH":
                            self.ipOB.AddPortOb((dstIP, dstPort), dstPortDesc)

                    elif transport == "UDP":
                        '''
                         0                   1                   2                   3
                         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
                         +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                         |          Source Port          |        Destination Port       |
                         +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                         |             Length            |            Checksum           |
                         +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                         '''

                        udpPacket = udp.UDP(unhexlify(ipPacket.payload))

                        timeStruct = time.gmtime(pkt.timestamp)

                        # extract the hour the packet was captured
                        theHour = timeStruct.tm_hour

                        ''' Your Code Goes here '''
                        srcPort = udpPacket.src_port
                        dstPort = udpPacket.dst_port

                        # Lookup Port Description, if not found assume Ephemeral
                        srcPortDesc = self.portOBJ.lookup(str(srcPort), "UDP")
                        if srcPortDesc == "EPH":
                            srcPort = "EPH"
                        else:
                            srcPort = str(srcPort)

                        dstPortDesc = self.portOBJ.lookup(str(dstPort), "UDP")
                        if dstPortDesc == "EPH":
                            dstPort = "EPH"
                        else:
                            dstPort = str(dstPort)

                         # Add a new IP observation and the hour
                        self.ipOB.AddOb(
                            (srcIP, dstIP, srcPort, dstPort, "UDP"), macData, theHour)

                        # Post them to PortObject Dictionary
                        if srcPort != "EPH":
                            self.ipOB.AddPortOb((srcIP, srcPort), srcPortDesc)
                        if dstPort != "EPH":
                            self.ipOB.AddPortOb((dstIP, dstPort), dstPortDesc)

                    elif transport == "ICMP":
                        '''
                         0                   1                   2                   3
                         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
                         +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                         |      Type     |      Code     |            Checksum           |
                         +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                         |                                                               |
                         +                          Message Body                         +
                         |                                                               |
                         +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                         '''

                        timeStruct = time.gmtime(pkt.timestamp)

                        # extract the hour the packet was captured
                        theHour = timeStruct.tm_hour

                        ''' YOUR CODE GOES HERE '''

                        self.ipOB.AddOb(
                            (srcIP, dstIP, "", "", "ICMP"), macData, theHour)

                elif frameType == "ARP":
                    '''
                    0                   1
                    0 1 2 3 4 5 6 7 8 9 0 1 2 3
                    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                    |  Dst-MAC  |  Src-MAC  |TYP|
                    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                    |                           |
                    +       Request-Reply       +
                    |                           |
                    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                    |        PAD        |  CRC  |
                    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                     '''

                    serverIP = srcIP
                    clientIP = dstIP

                    timeStruct = time.gmtime(pkt.timestamp)

                    # extract the hour the packet was captured
                    theHour = timeStruct.tm_hour

                    # Add a new IP observation and the hour
                    self.ipOB.AddOb(
                        (srcIP, dstIP, "", "", "ARP"), macData, theHour)

                else:
                    ''' frame type is not supported '''
                    continue

                newProgress = int(round((pktCnt / totPackets * 100)))

                if newProgress > 100:
                    newProgress = 100

                if newProgress > currentProgress:
                    self.progressBar['value'] = newProgress
                    currentProgress = newProgress
                    self.update()

            endTime = GetTime()

            # CREATE THE HTML RESULT

            tar = self.targetPath
            org = self.entryOrganization.get()
            ana = self.entryAnalyst.get()
            base = self.entryBaseline.get()

            self.mapReport = self.ipOB.CreateHTML(
                self.ReportFolder, startTime, endTime, "{:,}".format(pktCnt), tar, org, ana, base)
            self.ipOB.SaveOb(self.BaselinePath)

            # Once all packets have been processed update the status bar
            self.statusText['text'] = "Asset Map Complete: "
            LogEvent("Asset Map Complete")

            self.htmlButton['state'] = NORMAL
            self.update()

        else:
            self.statusText['text'] = "Status: Scan Failed, Cannot process target file: "+self.targetPath
            self.update()

    '''
    Display the generated HTML Report
    '''

    def btnViewReport(self):

        if platform.system() == 'Darwin':
            os.system("open /Applications/Safari.app "+self.mapReport)
        else:
            curDir = os.getcwd()
            url = curDir+self.mapReport[1:]
            webbrowser.open(url)

    '''
    STOP Scanning clicked
    '''

    def menuToolsExit(self, event=True):

        if messagebox.askokcancel("Exit Request", "Exit Search?"):
            LogEvent("Program Exit via Menu Selection")
            self.parent.destroy()
        else:
            pass

    '''
    User About Selected
    '''

    def menuAbout(self, event=True):
        NL = "\n"
        gMsgL1 = "Welcome to Python Forensics - Passive Network Mapping"
        gMsgL2 = "Version .75 Experimental - PCAP File Based Mapping"
        gMsgL3 = "Copyright 2016-2017 Python Forensics, Inc."
        gMsgL4 = "All Rights Reservered"
        messagebox.showinfo("About", gMsgL1+NL+gMsgL2+NL+gMsgL3+NL+gMsgL4+NL)
        messagebox.Dialog


'''
Setup a Protocol Handler to catch a User Exit
and prompt user to confirm exit
'''


def protocolhandler():
    if messagebox.askokcancel("Exit Request", "Exit PyMap?"):
        root.destroy()
    else:
        pass


'''
Search main program loop

- Establish the Root Application Window
- Establish the main window geometry and background
- Establish the run-time loop

'''
# Initialize the root TK Window
root = Tk()


def main():

    # Initialize the Forensic Log
    InitLog()

    # Specify the Main Window Icon
    # Select ico file for Windows
    if os.name == 'nt':
        root.iconbitmap(bitmap='search.ico')
    # Select png file, otherwise
    else:
        try:
            root.iconphoto(PhotoImage('search.xbm'))
        except Exception as e:
            print(e)

    # Set the Title for the Main Window
    root.title(TITLE)

    # Instantiate the GUI Application Object
    app = Application(root)

    # Setup and event handler if clicks to exit the main windowregex
    root.protocol("WM_DELETE_WINDOW", protocolhandler)

    # Start App MainLoop
    app.mainloop()


# Main Script Starts Here

if __name__ == '__main__':
    main()
