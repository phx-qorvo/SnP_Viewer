#Modules used
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

class UserInterface(Frame):    
    #User can get up to 3 folders worth of data
    def data_set(self):
        self.filez = tkFileDialog.askopenfilenames(title='Choose 1st set of files')        
        self.quit
    #called inside init so, it runs right away   
    def createwidgets(self):    
        # Buttons
        self.QUIT = Button(self)
        self.QUIT["text"] = "GO"
        self.QUIT["bg"]   = "Green"
        self.QUIT["command"] =  self.quit
        self.QUIT.grid(row=0,column=0)

        self.getfiles1 = Button(self)
        self.getfiles1["text"] = "Raw .snp files"
        self.getfiles1["command"] = self.data_set  
        self.getfiles1.grid(row=1,column=0)


        # Column Inputs
        self.portBox = Checkbutton(self, variable = self.customColumns,
                                   state = ACTIVE,
                                   text = 'Custom Columns?')

        self.portBox.grid(row=0,column=1)

        Label(self, text="Custom Column 1 Title: ").grid(row=1,column=1)
        self.column1Name = Entry(self)
        self.column1Name.insert(0, 'Board')
        self.column1Name.grid(row=1, column=2)

        Label(self, text="Custom Column 1 Data: ").grid(row=2, column=1)
        self.column1Data = Entry(self)
        self.column1Data.insert(0, 'One')
        self.column1Data.grid(row=2, column=2)

        # Column Inputs
        Label(self, text="Custom Column 2 Title: ").grid(row=1, column=3)
        self.column2Name = Entry(self)
        self.column2Name.insert(0, 'Unit')
        self.column2Name.grid(row=1, column=4)

        Label(self, text="Custom Column 1 Data: ").grid(row=2, column=3)
        self.column2Data = Entry(self)
        self.column2Data.insert(0, 'One')
        self.column2Data.grid(row=2, column=4)

        #always runs at initiaiton of class instance (python standard)
    def __init__(self, master=None):  
        Frame.__init__(self, master)
        self.portBox = Checkbutton()
        self.customColumns = BooleanVar()

        # self.column2Name = StringVar()
        # self.column1Name = StringVar()
        # self.column1Data = StringVar()
        # self.column2Data = StringVar()
        #
        #
        # self.column2Name = StringVar()
        # self.column1Name = StringVar()
        # self.column1Data = StringVar()
        # self.column2Data = StringVar()
        # self.column2Name.set("Unit")
        # self.column2Data.set("One")
        # self.column1Name.set("Board")
        # self.column1Data.set("One")


        master.title("User Interface")
        self.grid()
        self.createwidgets() 


