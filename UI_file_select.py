#Modules used
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import json
import os

class UserInterface(Frame):    
    #User can get up to 3 folders worth of data
    def data_set(self):
        self.filez = tkFileDialog.askopenfilenames(title='Choose 1st set of files',
                                                   initialdir = self.settingsDict['filesDir'])

    def SaveDirectory(self):
        self.outDirectory = tkFileDialog.askdirectory(title='Save Directory',
                                                      initialdir = self.settingsDict['saveDir'])

    def exit(self):
        #save settings to file
        self.settingsDict['Col1Title']=self.column1Name.get()
        self.settingsDict['Col2Title']=self.column2Name.get()
        self.settingsDict['Col1Data'] =self.column1Data.get()
        self.settingsDict['Col2Data'] =self.column2Data.get()
        self.settingsDict['saveDir']  =self.outDirectory
        if len(self.filez)==0:
            print "You didnt select any files"
            return

        path,filename = os.path.split(self.filez[0])
        self.settingsDict['filesDir'] =path
        print self.settingsDict
        with open('settings.json','w') as f:
            json.dump(self.settingsDict,f)
        self.quit()

    #called inside init so, it runs right away   
    def createwidgets(self):    
        # Buttons
        self.QUIT = Button(self)
        self.QUIT["text"] = "GO"
        self.QUIT["bg"]   = "Green"
        self.QUIT["command"] =  self.exit
        self.QUIT.grid(row=0,column=0)

        self.getfiles1 = Button(self)
        self.getfiles1["text"] = "Raw .snp files"
        self.getfiles1["command"] = self.data_set  
        self.getfiles1.grid(row=1,column=0)

        self.getDirectory = Button(self)
        self.getDirectory["text"] = "Save Directory?"
        self.getDirectory["command"] = self.SaveDirectory
        self.getDirectory.grid(row=2, column=0)

        # Column Inputs
        self.portBox = Checkbutton(self, variable = self.append,
                                   state = ACTIVE,
                                   text = 'Append?')

        self.portBox.grid(row=0,column=1)

        Label(self, text="Custom Column 1 Title: ").grid(row=1,column=1)
        self.column1Name = Entry(self)
        self.column1Name.insert(0, self.settingsDict['Col1Title'])
        self.column1Name.grid(row=1, column=2)

        Label(self, text="Custom Column 1 Data: ").grid(row=2, column=1)
        self.column1Data = Entry(self)
        self.column1Data.insert(0, self.settingsDict['Col1Data'])
        self.column1Data.grid(row=2, column=2)

        # Column Inputs
        Label(self, text="Custom Column 2 Title: ").grid(row=1, column=3)
        self.column2Name = Entry(self)
        self.column2Name.insert(0, self.settingsDict['Col2Title'])
        self.column2Name.grid(row=1, column=4)

        Label(self, text="Custom Column 1 Data: ").grid(row=2, column=3)
        self.column2Data = Entry(self)
        self.column2Data.insert(0, self.settingsDict['Col2Data'])
        self.column2Data.grid(row=2, column=4)

        #always runs at initiaiton of class instance (python standard)
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.portBox = Checkbutton()
        self.append = BooleanVar()
        self.append.set(0)
        self.outDirectory  = None
        self.filez         = []
        self.settingsDict = {}
        self.settingsDict['Col1Title'] = 'Build'
        self.settingsDict['Col2Title'] = 'Unit'
        self.settingsDict['Col1Data']  = 'One'
        self.settingsDict['Col2Data']  = 'One'
        self.settingsDict['saveDir'] = os.path.expanduser('~')
        self.settingsDict['filesDir'] = os.path.expanduser('~')


        try:
            with open('settings.json','r') as f:
                self.settingsDict = json.load(f)

        except ValueError:
            print 'could not read file'

        except IOError:
            print 'File doent exist yet'

        master.title("User Interface")
        self.grid()
        self.createwidgets() 


