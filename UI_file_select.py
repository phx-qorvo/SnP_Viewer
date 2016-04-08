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
        self.QUIT.grid(row=4,column=0)

        self.getfiles1 = Button(self)
        self.getfiles1["text"] = "Raw .snp files"
        self.getfiles1["command"] = self.data_set  
        self.getfiles1.grid(row=2,column=0)
        
        
    #always runs at initiaiton of class instance (python standard)    
    def __init__(self, master=None):  
        Frame.__init__(self, master)
        self.linearitytarget = 0
        self.Order           = 1
        self.filez1          =[]
        self.filez2          =[]
        self.filez3          =[]  
        self.pdf_pages       =[]  
        self.spec            =[]
        self.start           =0
        self.stop            =0
        master.title("User Interface")
        self.grid()
        self.createwidgets() 


