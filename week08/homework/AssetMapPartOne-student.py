'''
PART I - ASSETMAP-GUI
'''
# Python Standard Library Module Imports

import sys               # System specifics
import os                # Operating/Filesystem Module
import time              # Basic Time Module

'''
Python Core GUI Library 
tkinter GUI Components from the Standard Library
'''
from   tkinter import *  # TK GUI Components
from   tkinter import messagebox
from   tkinter import ttk
from   tkinter import filedialog
from   tkinter import Tk
import tkinter.font as tkfont

# Script Constants

NAME    = "PYTHON ASSET-MAP - "
VERSION = "PART I"
AUTHOR  = "YOUR NAME"
TITLE   = NAME+'\t'+VERSION
DEBUG   = False

# Screen Colors
BG = 'white'
FG = 'black'


class Application(Frame):
    '''
    APPLICATION CLASS GUI FRAME USING TKINKER
    Establish the GUI Environment
    '''    

    def __init__(self, master=None):

        # Define the instance variables to be
        # collected from the GUI

        self.targetPath   = "./PCAP/"
        self.ReportFolder = "./REPORTS/"
        self.BaselinePath = "./BASELINES/"
        self.abortFlag    = False
        
        try:
            if not os.path.exists(self.targetPath):
                os.mkdir(self.targetPath)
                
            if not os.path.exists(self.ReportFolder):
                os.mkdir(self.ReportFolder)
                
            if not os.path.exists(self.BaselinePath):
                os.mkdir(self.BaselinePath)                    

        except Exception as err:
            sys.exit("\n\nScript Aborted, cannot create target folders")
            

        # Create the basic frame
        Frame.__init__(self, master)
        self.parent = master

        self.parent.resizable(0,0)

        # Intialize the GUI
        self.initUI()

    def initUI(self):
        '''
        Initialize the GUI components
        - Menu Bar
        - Root Folder Selection
        - Perform Search Button
        - Status Bar
        '''        

        # Create Menu Bar
        menuBar = Menu(self.parent)  # menu begin
        toolsMenu = Menu(menuBar, tearoff=0)

        toolsMenu.add_command(label='About Search', accelerator='Ctrl+A', command=self.menuAbout, underline=0)
        toolsMenu.add_separator()
        toolsMenu.add_command(label='Exit', accelerator='Ctrl+X', command=self.menuToolsExit)
        menuBar.add_cascade(label='Help', menu=toolsMenu, underline=0)   
        self.parent.config(menu=menuBar)  # menu ends
        self.bind_all("<Control-x>", self.menuToolsExit)
        self.bind_all("<Control-a>", self.menuAbout)

        # Case Investigator
        self.investigatorValue = Label(self.parent, anchor='w', text="Analyst: ")
        self.investigatorValue.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    
        self.nValue = StringVar()
        self.nValue = ''
        self.entryAnalyst=Entry(self.parent,textvariable=self.nValue,width=50)
        self.entryAnalyst.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    
        # Investigator Organization
        ''' your code goes here 
            Modeling your code after Case Investiator section above
            add the ability for the user to type in the 
            investigator Organization using a width of 50
        '''
    
        # Baseline Description
        ''' your code goes here 
            Modeling your code after Case Investiator section above
            add the ability for the user to type in the baseline name
            again with a width of 50
        '''

        # Target File to Search
        self.lblTarget = Label(self.parent, anchor='w', text="Target PCAP")
        self.lblTarget.grid(row=3, column=0, padx=5, pady=10, sticky='w')

        self.targetFile= Label(self.parent, anchor='w', bd=3, bg = 'white', fg='black',width=60, relief=SUNKEN)     
        self.targetFile.grid(row=3, column=1, padx=5, pady=0, sticky='w')

        self.buttonTargetFile = Button(self.parent, text=' ... ', command=self.btnSelectFile, width=5, bg ='gray', fg='white', activebackground='black', activeforeground='green')
        self.buttonTargetFile.grid(row=3, column=2, padx=5, pady=0, sticky='w')
        
        # Create Asset Map Button
        self.searchButton = Button(self.parent, text='Create Asset Map', command=self.btnCreateAssetMap, bg ='gray', fg='white', activebackground='black', activeforeground='green')
        self.searchButton.grid(row=4, column=1, padx=5, pady=5, sticky=W)

        # Display HTML results Button
        ''' your code goes here 
            Modeling your code after Create Asset Mapp Button above
            add a new Button with the text="View Report
            Place the button as shown in the provided screenshot
            When the button is pressed it will launch the self.btnViewReport method
            again model this after the Asset Button Method above
        '''      
        
        # Create Status Bar
        self.statusText = Label(self.parent, anchor='w', width=80, bd=3, bg = 'white', fg='black', relief=SUNKEN)     
        self.statusText.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky='w')
        
        self.statusText['text'] = "Waiting... Please select target pcap file"

        self.update()

    '''
    ALL Button and EVENT HANDLERS
    Code Area
    '''

    def btnSelectFile(self):
        
        # Handle Folder Browse Button Click       
        fileName = filedialog.askopenfilename(initialdir="./PCAP/",  title='Select a file to Search')
        self.targetFile['text'] = fileName    
        self.targetPath = fileName
        
        if self.targetPath:   
            self.statusText['text'] = "Target File Selected: "+self.targetPath
            self.update()

    def btnCreateAssetMap(self):
        # Handle Create Asset Map Button Click
        pcapFile = self.targetFile['text']
        if pcapFile:
            self.statusText['text'] = "PCAP PROCESSED ... "   
            self.update()       
        else:
            self.statusText['text'] = "PCAP NOT SELECTED ... "   
            self.update()                 

    def btnViewReport(self):
        # Handle Perform DISPLAY HTML Button Click
        '''
        Your Code Goes Here
        Model this after the btnCreate AssetMap method above
        '''
        self.update()

    def btnSTOPSearch(self):
        # Handle STOP Button Click
        self.statusText['text'] = "DISPLAY HTML RESULTS ... "   
        self.update()

    def menuToolsExit(self, event=True):
        # Handle Exit Click
        if messagebox.askokcancel("Exit Request", "Exit Search?"):
            self.parent.destroy()
        else:
            pass        

    def menuAbout(self, event=True):
        # Handle User About
        NL = "\n"
        gMsgL1 = "Experimental PCAP ASSET MAPPING"
        gMsgL2 = "Experimental - PCAP File Based Mapping"
        gMsgL3 = "Copyright 2020"
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
    
    # Specify the Main Window Icon
    root.iconbitmap('search.ico')
    
    # Set the Title for the Main Window
    root.title(TITLE)   

    # Instantiate the GUI Application Object
    app = Application(root)

    # Setup and event handler if clicks to exit the main window
    root.protocol("WM_DELETE_WINDOW", protocolhandler)

    # Start App MainLoop  
    app.mainloop()


# Main Script Starts Here

if __name__ == '__main__':
    main()
