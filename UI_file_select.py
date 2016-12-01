#Modules used
from tkinter import *
# import tkinter, tkconstants, tkFileDialog
import json
import tkinter.filedialog
import os

class UserInterface(Frame):
    def data_set(self):
        self.filez = tkinter.filedialog.askopenfilenames(title='Choose 1st set of files',
                                                   initialdir = self.settingsDict['filesDir'])

    def SaveDirectory(self):
        self.outDirectory = tkinter.filedialog.askdirectory(title='Save Directory',
                                                      initialdir = self.settingsDict['saveDir'])

    def exit(self):
        #save settings to file
        self.settingsDict['saveDir']  = self.outDirectory
        self.settingsDict['filesDir'] = os.path.split(self.filez[0])[0]
        if len(self.filez)==0:
            print("You didn't select any files")
            return
        if self.outDirectory==0:
            print("you didnt pick a place to save Files")
            return
        with open('settings.json','w') as f:
            json.dump(self.settingsDict,f)
        self.quit()

    def createwidgets(self):
        # Buttons
        self.QUIT["text"] = "GO"
        self.QUIT["bg"]   = "Green"
        self.QUIT["command"] =  self.exit
        self.QUIT.grid(row=0,column=0)

        self.getFiles["text"] = "Raw .snp files"
        self.getFiles["command"] = self.data_set
        self.getFiles.grid(row=1, column=0)
        self.getDirectory = Button(self)
        self.getDirectory["text"] = "Save Directory?"
        self.getDirectory["command"] = self.SaveDirectory
        self.getDirectory.grid(row=2, column=0)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.portBox = Checkbutton()
        self.append = BooleanVar()
        self.append.set(0)
        self.outDirectory  = None
        self.filez         = []
        self.getFiles = Button(self)
        self.QUIT = Button(self)
        self.settingsDict={}
        self.settingsDict['filesDir'] = ''
        self.settingsDict['saveDir'] = ''
        master.title("User Interface")
        self.grid()
        try:
            with open('settings.json','r') as f:
                self.settingsDict = json.load(f)
        except ValueError:
            print('could not read file')
        except IOError:
            print('File doent exist yet')
        self.createwidgets() 


