'''
MP3-ID3Forensics - Python 3 Version

Python Script (written completely in Python)
For the extraction of meta data and 
potential evidence hidden in MP3 files
specifically in the ID3 Headers 

Author C. Hosmer
       Python Forensics

Copyright (c) 2019 Chet Hosmer / Python Forensics, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

'''

# IMPORT MODULES

# Standard Python Libraries

import os                           # Standard Operating System Methods
import argparse                     # Command Line Argument Parsing
from   struct import *              # Handle Strings as Binary Data 
import string                       # Special string Module
import time                         # Date Time Module
import sys


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

def GetTime(timeStyle = "UTC"):

    if timeStyle == 'UTC':
        return ('UTC Time: ', time.asctime(time.gmtime(time.time()))) 
    else:
        return ('LOC Time: ', time.asctime(time.localtime(time.time())))

# End GetTime Function ============================    


#
# Print Hexidecimal / ASCII Page Heading
#

def PrintHeading():

    print("Offset        00  01  02  03  04  05  06  07  08  09  0A  0B  0C  0D  0E  0F        ASCII")
    print("------------------------------------------------------------------------------------------------")
    
    return

# End PrintHeading

#
# Print ID3 Frame Contents
#
# Input: buff - Holding the frame content
#        buffSize - Size of the frame contents
#

def PrintContents(buff, buffSize):
    
    PrintHeading()
    offset = 0
    
    # Loop through 1 line at a time
    
    for i in range(offset, offset+buffSize, 16):

        # Print the current offset    
        
        print ("%08x      " % i, end="")
        
        # Print 16 Hex Bytes
        for j in range(0,16):
            if i+j >= buffSize:
                print('    '*(16-j),end="")
                break
            else:
                byteValue = buff[i+j]
                print("%02x  " % byteValue,end="")
        print("      ",end="")
        
        # Print 16 Ascii equivelents
        
        for j in range (0,16):
            if i+j >= buffSize:
                break            
            byteValue = buff[i+j]
            # If printable characters print them
            if (byteValue >= 0x20 and byteValue <= 0x7f):
                print("%c" % byteValue,end="")
            else:
                print('.',end="")
        print()
    
    return

# End Print Buffer

'''
ID3 Class

Extracting Meta and Evidence from mp3 files

'''

class ID3():
    

#Class Constructor

    def __init__(self, theFile):
        
        # Initialize Attributes of the Object
        
        # Local Constants
    
        self.KNOWN_TAGS_V3 = {
            b'AENC': 'Audio encryption:                 ', 
            b'APIC': 'Attached picture:                 ', 
            b'COMM': 'Comments:                         ',
            b'COMR': 'Commercial frame:                 ',
            b'ENCR': 'Encryption method registration:   ',
            b'EQUA': 'Equalization:                     ',
            b'ETCO': 'Event timing codes:               ',
            b'GEOB': 'General encapsulated object:      ',
            b'GRID': 'Grp identification registration:  ',
            b'IPLS': 'Involved people list:             ',
            b'LINK': 'Linked information:               ',
            b'MCDI': 'Music CD identifier:              ',
            b'MLLT': 'MPEG location lookup table:       ',
            b'OWNE': 'Ownership frame:                  ',
            b'PRIV': 'Private frame:                    ',
            b'PCNT': 'Play counter:                     ',
            b'POPM': 'Popularimeter:                    ',
            b'POSS': 'Position synchronisation frame:   ',
            b'RBUF': 'Recommended buffer size:          ',
            b'RGAD': 'Replay Gain Adjustment:           ',
            b'RVAD': 'Relative volume adjustment:       ',
            b'RVRB': 'Reverb:                           ',
            b'SYLT': 'Synchronized lyric/text:          ',
            b'SYTC': 'Synchronized tempo codes:         ',
            b'TALB': 'Album/Movie/Show title:           ',
            b'TBPM': 'BPM beats per minute:             ',
            b'TCOM': 'Composer:                         ',
            b'TCON': 'Content type:                     ',
            b'TCOP': 'Copyright message:                ',
            b'TDAT': 'Date:                             ',
            b'TDLY': 'Playlist delay:                   ',
            b'TDRC': 'Recording Time:                   ',
            b'TENC': 'Encoded by:                       ',
            b'TEXT': 'Lyricist/Text writer:             ',
            b'TFLT': 'File type:                        ',
            b'TIME': 'Time:                             ',
            b'TIT1': 'Content group description:        ',
            b'TIT2': 'Title/songname/content descrip:   ',
            b'TIT3': 'Subtitle/Description refinement:  ',
            b'TKEY': 'Initial key:                      ',
            b'TLAN': 'Language:                         ',
            b'TLEN': 'Length:                           ',
            b'TMED': 'Media type:                       ',
            b'TOAL': 'Original album/movie/show title:  ',
            b'TOFN': 'Original filename:                ',
            b'TOLY': 'Original lyricist/text writer:    ',
            b'TOPE': 'Original artist/performer:        ',
            b'TORY': 'Original release year:            ',
            b'TOWN': 'File owner/licensee:              ',
            b'TPE1': 'Lead performer/Soloist:           ',
            b'TPE2': 'Band/orchestra/accompaniment:     ',
            b'TPE3': 'Conductor/performer refinement:   ',
            b'TPE4': 'Interpreted, remixed, modified by:',
            b'TPOS': 'Part of a set:                    ',
            b'TPUB': 'Publisher:                        ',
            b'TRCK': 'Track number/Position in set:     ',
            b'TRDA': 'Recording dates:                  ',
            b'TRSN': 'Internet radio station name:      ',
            b'TRSO': 'Internet radio station owner:     ',
            b'TSIZ': 'Size:                             ',
            b'TSRC': 'Intl standard recording code:     ',
            b'TSSE': 'SW/HW settings used for encoding: ',                         
            b'TYER': 'User defined text frame:          ',
            b'TXXX': 'User define general text frame:   ',
            b'UFID': 'Unique file identifier:           ',
            b'USER': 'Terms of use:                     ',
            b'USLT': 'Unsyched lyric/text transcription:',
            b'WCOM': 'Commercial information:           ',
            b'WCOP': 'Copyright/Legal informationL      ',
            b'WOAF': 'Official audio file webpage:      ',
            b'WOAR': 'Official artist/performer webpage:',
            b'WOAS': 'Official audio source webpage:    ',
            b'WORS': 'Official internet radio homepage: ',
            b'WPAY': 'Payment:                          ',
            b'WPUB': 'Publishers official webpage:      ',
            b'WXXX': 'User defined URL link frame:      '
        }

        self.KNOWN_TAGS_V2 = {
            'BUF': 'Recommended buffer size',
            'COM': 'Comments',
            'CNT': 'Play counter',
            'CRA': 'Audio Encryption',
            'CRM': 'Encrypted meta frame',
            'ETC': 'Event timing codes',
            'EQU': 'Equalization',
            'GEO': 'General encapsulated object',
            'IPL': 'Involved people list',
            'LNK': 'Linked information',
            'MCI': 'Music CD Identifier',
            'MLL': 'MPEG location lookup table',
            'PIC': 'Attached picture',
            'POP': 'Popularimeter',
            'REV': 'Reverb',
            'RVA': 'Relative volume adjustment',
            'SLT': 'Synchronized lyric/text',
            'STC': 'Synced tempo codes',
            'TAL': 'Album/Movie/Show title',
            'TBP': 'BPM Beats Per Minute',
            'TCM': 'Composer',
            'TCO': 'Content type',
            'TCR': 'Copyright message',
            'TDA': 'Date',
            'TDY': 'Playlist delay',
            'TEN': 'Encoded by',
            'TFT': 'File type',
            'TIM': 'Time',
            'TKE': 'Initial key',
            'TLA': 'Languages',
            'TLE': 'Length',
            'TMT': 'Media type',
            'TOA': 'Original artists/performers',
            'TOF': 'Original filename',
            'TOL': 'Original Lyricists/text writers',
            'TOR': 'Original release year',
            'TOT': 'Original album/Movie/Show title',
            'TP1': 'Lead artist(s)/Lead performer(s)/Soloist(s)/Performing group',
            'TP2': 'Band/Orchestra/Accompaniment',
            'TP3': 'Conductor/Performer refinement',
            'TP4': 'Interpreted, remixed, or otherwise modified by',
            'TPA': 'Part of a set',
            'TPB': 'Publisher',
            'TRC': 'International Standard Recording Code',
            'TRD': 'Recording dates',
            'TRK': 'Track number/Position in set',      
            'TSI': 'Size',
            'TSS': 'Software/hardware and settings used for encoding',
            'TT1': 'Content group description',
            'TT2': 'Title/Songname/Content description',
            'TT3': 'Subtitle/Description refinement',
            'TXT': 'Lyricist/text writer',
            'TXX': 'Year',
            'UFI': 'Unique file identifier',
            'ULT': 'Unsychronized lyric/text transcription',
            'WAF': 'Official audio file webpage',
            'WAR': 'Official artist/performer webpage',
            'WAS': 'Official audio source webpage',
            'WCM': 'Commercial information',
            'WCP': 'Copyright/Legal information',
            'WPB': 'Publishers official webpage',
            'WXX': 'User defined URL link frame'
        }
        
        self.picTypeList = [
                       'Other',
                       'fileIcon',
                       'OtherIcon',
                       'FrontCover',
                       'BackCover',
                       'LeafletPage',
                       'Media',
                       'LeadArtist',
                       'ArtistPerformer',
                       'Conductor',
                       'BandOrchestra',
                       'Composer',
                       'Lyricist',
                       'RecordingLocation',
                       'DuringRecording',
                       'DuringPerformance',
                       'MovieScreenCapture',
                       'Fish',
                       'Illustration',
                       'BandArtistLogo',
                       'PublisherStudioLogo'
                      ]

        # Attributes of the Class 
        
        self.fileName        = ''
        self.id3Size         = 0
        self.fileContents    = ''
        
        self.mp3             = False
        self.id3             = False
        
        self.hdr             = ''
        self.flag            = 0 
        self.version         = 0  
        self.revision        = 0

        self.unsync          = False
        self.extendedHeader  = False 
        self.experimental    = False
        
        self.hasPicture      = False
        self.imageCount      = 0
        
        self.frameList       = []
        
        self.padArea         = ''
     
        # Now Process the Proposed MP3 File
    
        try:
            self.fileName = theFile
            with open(theFile, 'rb') as mp3File:    
                self.fileContents = mp3File.read()
        except Exception as err:
            print("Could not process input file: ", theFile, err)
            quit()

        #Strip off the first 10 characters of the file
        stripHeader = self.fileContents[0:6]  
    
        #now unpack the header
        id3Header = unpack('3sBBB', stripHeader)
    
        self.hdr         = id3Header[0]
        self.version     = id3Header[1]
        self.revision    = id3Header[2]
        self.flag        = id3Header[3]
        
        if (self.hdr == 'ID3' or self.hdr == b'ID3') and self.version in range(2,5):
            self.id3 = True
        else:
            self.id3 = False
            print("MP3 File type not supported")
            quit()
        
        # If we seem to have a valid MP3 ID3 Header
        # Attempt to Process the Header
        
        # Get Size Bytes and unpack them
        stripSize = self.fileContents[6:10]    
        
        id3Size = unpack('BBBB', stripSize)
        
        # Calculate the Size (this is a bit tricky)
        # and add in the 10 byte header not included
        # in the size
        
        self.id3Size = self.calcID3Size(id3Size) + 10    
        
        # check the unsync flag
        if self.flag & 0x60:
            self.unsync = True
        
        # check the extended header flag
        if self.flag & 0x40:
            self.extendedHeader = True
        
        # check the experimental indicator
        if self.flag & 0x40:
            self.experimental = True             
        
        self.processID3Frames()
        
        return 
    
    '''
    Print out any extracted header information
    '''
        
    def printResults(self):
        print("==== MP3/ID3 Header Information")
        print("ID3 Found:       ", self.id3)
        
        if self.id3:
            print("File:            ", self.fileName)
            print("ID3 Hdr Size:    ", self.hdr)
            print("Version:         ", self.version)
            print("Revision:        ", self.revision)
            print("Size:            ", self.id3Size)
            print("Unsync           ", self.unsync)
            print("Extended Header: ", self.extendedHeader)
            print("Experimental:    ", self.experimental)
            print("Images Found:    ", str(self.imageCount))
            print("\n------------------------------------------------------------------------")   
            print("ID3 Frames")
            print("------------------------------------------------------------------------")
            
            for entry in self.frameList:
                print("FrameID: ", entry[0])
                print("Frame Type:        ", entry[1])
                print("Frame Size:        ", entry[2])

                print("Tag  Preservation: ", entry[4])
                print("File Preservation: ", entry[5])
                print("Read Only:         ", entry[6])
                print("Compressed:        ", entry[7])
                print("Encrypted:         ", entry[8])
                print("Group Identity:    ", entry[9])
                print("\nFrame Content:\n")
                PrintContents(entry[3], len(entry[3]))
                print("====================================================================================================\n")
                
            print("\nPad Area - Size", len(self.padArea)) 
            if len(self.padArea) != 0:
                PrintContents(self.padArea, len(self.padArea))
                
            print("\n\n END PyMP3 Forensics")
            
    def processID3Frames(self):
            
        if self.id3:
            
            # starting first frame location
            frameOffset = 10
            imageCount = 0
            
            # Loop Through all the frames until we reach 
            # Null ID
            
            # while self.fileContents[frameOffset] != '\000':
            
            while frameOffset < self.id3Size:
                
                # check for padding
                if self.fileContents[frameOffset] == 0:
                    # we are at the end of the frame
                    # and we have found padding
                    # record the pad area
            
                    self.padArea = self.fileContents[frameOffset:self.id3Size]
                    break
                
                if self.version == 2:
            
                    # Version 2 Headers contain 
                    # 6 bytes
                    # sss = type
                    # xxx = size
            
                    frameID     = self.fileContents[frameOffset:frameOffset+3]
                      
                    if frameID in self.KNOWN_TAGS_V2:
                        frameDescription = self.KNOWN_TAGS_V2[frameID]
                    else:
                        frameDescription = 'Unknown'      
                        
                    frameOffset +=3
                    stripSize   = self.fileContents[frameOffset:frameOffset+3]   
                    frameOffset +=3
                    frameSize   = unpack('BBB', stripSize)
                    
                    integerFrameSize = self.calcFrameSize(frameSize)
                    
                    # If the frame is a picture
                    # extract the contents of the picture and create
                    # a separate file
                    
                    if frameID == "PIC":
                        self.hasPicture = True     
                        # bump the image count in case multiple images
                        # are included in this file                              
                        self.imageCount+=1
                        self.extractPicture(frameOffset, 2, integerFrameSize, self.imageCount)
                                                
                    # For version 2 set all version 3 flags to False
                    tagPreservation  = False
                    filePreservation = False
                    readOnly         = False
                    compressed       = False
                    encrypted        = False
                    groupID          = 0
            
                elif self.version == 3 or self.version == 4:
            
                    # Version 3 Headers contain
                    # 10 Bytes
                    # ssss = Type
                    # xxxx = size 
                    # xx   = flags
            
                    v3Header = self.fileContents[frameOffset:frameOffset+10]
                    frameOffset += 10
                    try:
                        frameHeader = unpack('!4sIBB', v3Header)
                    except:
                        print("Unpack Failed")
                        quit()
            
                    frameID          = frameHeader[0]
                    integerFrameSize = frameHeader[1]
                    flag1            = frameHeader[2]
                    flag2            = frameHeader[3]  
                    
                    if frameID == b'APIC':
                        self.hasPicture = True     
                        # bump the image count in case multiple images
                        # are included in this file                        
                        self.imageCount+=1
                        self.extractPicture(frameOffset, 3, integerFrameSize, self.imageCount)
                                             
                    if frameID in self.KNOWN_TAGS_V3:
                        frameDescription = self.KNOWN_TAGS_V3[frameID]
                    else:
                        frameDescription = 'Unknown'
                        
                    if flag1 & 0x80:
                        tagPreservation = False
                    else:
                        tagPreservation = True
                        
                    if flag1 & 0x60:
                        filePreservation = False
                    else:
                        filePreservation = True
                        
                    if flag1 & 0x40:
                        readOnly = True
                    else:
                        readOnly = False
                        
                        
                    if flag2 & 0x80:
                        compressed = True
                    else:
                        compressed = False
                        
                    if flag2 & 0x60:
                        encrypted = True
                    else:
                        encrypted = False
                        
                    if flag2 & 0x40:
                        groupId = True
                    else:
                        groupID = False                    
            
                else:
                    print("Version Not Supported")
                    quit()
            
                
                frameContent = self.fileContents[frameOffset:frameOffset+integerFrameSize]  
                frameOffset += integerFrameSize
                
                # Add frame information
                self.frameList.append([frameID, frameDescription, integerFrameSize, frameContent, tagPreservation, filePreservation, readOnly, compressed, encrypted, groupID] )

                print(frameID.decode('utf-8'), frameDescription,end="")
                                
                if frameContent[0] == 0:
                    frameDump = frameContent[1:]     
                else:
                    frameDump = frameContent
                    
                frameSnip = ''
                
                if frameID == "COMM" or frameID == "TXXX":
                    for eachChar in frameDump:
                        if eachChar in string.printable:
                            frameSnip = frameSnip + eachChar 
                        else:
                            continue               
                else:
                    for eachChar in frameDump:
                        eachChar = chr(eachChar)
                        if eachChar in string.printable:
                            frameSnip = frameSnip + eachChar 
                        else:
                            break
                        
                if frameSnip.startswith('XXX'):
                    frameSnip = frameSnip[3:]
                    
                print(frameSnip[0:80])
                print()
            return

    '''
    extractPicture from ID3 Frame
    
    input: offset to the frame
           version (2 or 3)
           
           writes output to an images directory
           note the images directory must exist
           ./images/  
           
    '''
    
    def extractPicture(self, off, ver, lenOfFrame, imgCnt):
                  
        jpegBegin = 0
        
        for x in range(off, off+24):
            eachByte = self.fileContents[x]
            if eachByte == 0xff:
                if self.fileContents[x+1] == 0xd8:
                    jpegBegin = x
                    break
        
        if jpegBegin != 0:
 
            # Extract the picture from the content
            thePicture = self.fileContents[jpegBegin:off+lenOfFrame]
            
            # Create a unique name for the picture relating it back to the original
            # filename into a sub-directory named images
            
            imageName = "./images/"+os.path.basename(self.fileName)+'-'+str(imgCnt)+'.jpg'

            # Open the file for writing and write out the content
            with open(imageName, "wb") as out:
                out.write(thePicture)
        else:
            # Note a jpeg abort
            return                   
        
    
    
    
    '''
    Calculate the ID3 Size
    
       The ID3 Size is 28 bits spread over 4 bytes in Big Endian Format
       the MSB of each byte is ignored and the remaining 7 bits of each byte are 
       concatenated together to produce a 28 bit string.
    
       For example the four byte size shown below:
    
       0x0 0x1 0x4a 0x3
    
       Creates the following 28 bit string
    
       0000000000000110010100000011
    
       for a decimal integer value of:
    
       25859  
    
       Adding in the 10 header bytes (which is not included in the size)
       the total size is:
    
       25869
    
       Excerpt from ID3 Standard
    
       The ID3 tag size is the size of the complete tag after
       unsychronisation, including padding, excluding the header (total tag
       size - 10). The reason to use 28 bits (representing up to 256MB) for
       size description is that we don't want to run out of space here.
    
       calcID3Size(receives a tuple of the four bytes)
    '''
    
    def calcID3Size(self, bytes): 
    
        # Convert the tuple to a list for easy processing
    
        bytes = list(bytes)
    
        # Ensure that the MSB of each Byte is zero
    
        bytes[0] = bytes[0] & 0x7f
        bytes[1] = bytes[1] & 0x7f
        bytes[2] = bytes[2] & 0x7f
        bytes[3] = bytes[3] & 0x7f
    
        # Initialize the bit string we will create
        bits = ""
    
        # loop through each byte setting each 
        # to a '1' or '0' starting with bit 6
    
        for val in bytes:
    
            i = 64
    
            # continue until we process all bits 
            # from bit 6-0
    
            while i > 0:
                if val & i:
                    bits = bits + '1'
                else:
                    bits = bits + '0'
    
                # move to the next lower bit
                i = i >> 1
    
        # Now simply Convert the Binary String to an Integer
    
        integerSize = int(bits,2)
    
        return integerSize
    
    '''
    Calculate the Frame size from the 3 hex bytes provided
    
    Excerpt from ID3v2 Standard
    
       The three character frame identifier is followed by a three byte size
       descriptor, making a total header size of six bytes in every frame.
       The size is calculated as framesize excluding frame identifier and
       size descriptor (frame size - 6).
    
    calcFrameSize(receives a tuple of the three bytes)
    
    '''
    
    def calcFrameSize(self, bytes):
    
        valList = list(bytes)
    
        finalValue = valList[0] << 16
        finalValue = finalValue | valList[1] << 8
        finalValue = finalValue | valList[2]
    
        return finalValue    

''' 
Main Program
'''
def main():
    print()
    print("Python Forensics, Inc.  www.python-forensics.org")
    print("Python MP3 Forensics v2.0 May 2019 Python 3.x Version")
    print("developed by: C. Hosmer")
    print()
    print("Script Started", GetTime())
    print()
    
    # Process the command line arguments
    
    parser = argparse.ArgumentParser()
    parser.add_argument('mp3File')
    theArgs = parser.parse_args()
     
    # Obtain the single argument which is the 
    # full path name of the file to process
    
    mp3File = theArgs.mp3File
    
    # Verify the file exists and is a file
    if not os.path.isfile(mp3File):
        sys.exit(mp3File+" Not Found")
    
    # Verify we have a valid output directory for images
    curDir = os.getcwd()
    if not os.path.isdir("./images"):
        # if not then attempt to create it.
        try:
            os.mkdir("./images")
        except Exception as err:
            sys.exit("Cannot create output directory: "+err)
        
    # set the output to verbose
    verbose = True
    
    print("Processing MP3 File: ", mp3File)
    print()
    
    # Process the mp3File
    objID3 = ID3(mp3File)
    
    # If verbose is selected the print results to standard out
    # otherwise create a log file
    
    if objID3.id3:
        if verbose:
            objID3.printResults()
        else:
            # Turn on Logging
            logging.basicConfig(filename='pSearchLog.log',level=logging.DEBUG,format='%(asctime)s %(message)s')            
            objID3.logResults()
    
if __name__ == "__main__":
    main()