import _tkinter
import numpy as np
from scipy import interpolate
import os
import sip
from tkinter import *
import tkinter
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import matplotlib.cm as cm
import pandas as pd
import getpass
from Utils import smith
from Utils import moving_average
from Utils import power_gain
from Utils import vswr_circles
from Utils import spec_lines
from UI_file_select import UserInterface
from UI_snp_constraints import UserLimits
from convert_snp_to_pandas_df import convert_snp_csv
import py_syntax_highlighting


class SnpPlotter:

    def __init__(self):
        # *******************Setup interactive plotting*********************************
        self.app = QtGui.QApplication([])
        self.dataLayout = QtGui.QGridLayout()
        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.win.setLayout(self.dataLayout)
        self.win.resize(1000, 600)
        self.win.setWindowTitle('Smith_Charts')
        pg.setConfigOptions(antialias=True)  # Enable anti-aliasing for prettier plots
        #******************  Variable Definitions ***********************************
        self.plots={}
        self.df = pd.DataFrame  # where main bulk of data is stored
        self.colors = {}
        # **************************** Static Widgets ******************************
        self.radio = {}
        self.radioP = {}
        # Grab data
        self.dataButton = QtGui.QPushButton('Grab Data')
        self.dataButtonP = QtGui.QGraphicsProxyWidget()
        self.dataButtonP.setWidget(self.dataButton)
        self.dataButton.clicked.connect(self.GrabData)
        # add marker button
        self.markerButton = QtGui.QPushButton('Add Marker')
        self.markerButtonP = QtGui.QGraphicsProxyWidget()
        self.markerButtonP.setWidget(self.markerButton)
        # marker input frequency
        self.markerInput = QtGui.QLineEdit("Enter Frequency in MHz")
        self.markerInputP = QtGui.QGraphicsProxyWidget()
        self.markerInputP.setWidget(self.markerInput)
        # remove markers button
        self.markerRemove = QtGui.QPushButton('Remove Markers')
        self.markerRemoveP = QtGui.QGraphicsProxyWidget()
        self.markerRemoveP.setWidget(self.markerRemove)

        # Static widgets section
        self.dataWidget = QtGui.QGraphicsWidget()
        self.dataLayout = QtGui.QGraphicsGridLayout(self.dataWidget)
        self.dataLayout.addItem(self.dataButtonP, 0, 0)
        self.dataLayout.addItem(self.markerButtonP,0, 1)
        self.dataLayout.addItem(self.markerInputP, 0, 2)
        self.dataLayout.addItem(self.markerRemoveP,0,3)

        self.dataWidget.setLayout(self.dataLayout)
        self.win.addItem(self.dataWidget, 0, 0, 1, 1)
        self.win.nextRow()


    def GrabData(self):
        root = Tk()
        files = tkinter.filedialog.askopenfilenames(title='Choose 1st set of files')
        frames = []
        order = []
        for f in files:
            frames.append(convert_snp_csv(f))
            extension = os.path.splitext(f)[1]
            num = [int(s) for s in re.findall(r'\d+', extension)]  # get file extension
            order.append(num[0])  # get 'n' number associated with SnP  (order)
        self.df = pd.concat(frames)
        print(self.df.columns.tolist())
        maxPorts = max(order)
        portSelect = UserLimits(maxPorts, master=root)
        portSelect.mainloop()
        root.destroy()
        counter = 0
        self.plots={}
        for x in range(1,maxPorts+1):
            for y in range(1,maxPorts+1):
                if portSelect.plot[counter].get() == 1: #plot true/false
                    if portSelect.graph_type[counter].get()==1:
                        self.plots['dB_S' + str(x) + str(y)] = {}
                    else:
                        self.plots['Smith_S'+str(x)+str(y)]={}
                counter+=1
        self.DynamicWidgets()


    def DynamicWidgets(self):
        # dynamic widgets
        self.dynamicWidgets = QtGui.QGraphicsWidget()
        self.dynamicWidgetsLayout = QtGui.QGraphicsGridLayout(self.dynamicWidgets)
        self.colors={}
        self.radio={}
        self.radioP={}
        self.group = self.df.groupby('sourcefile')
        color_map = iter(cm.gist_rainbow(np.linspace(0, 1, len(self.group))))
        i = 0
        for key, g in self.group:
            red, green, blue, a = next(color_map)
            red = int(red * 255)
            green = int(green * 255)
            blue = int(blue * 255)
            self.colors[key] = QtGui.QColor(red, green, blue)
            self.radio[key] = QtGui.QCheckBox(key[-30:])
            self.radio[key].setStyleSheet('background-color:black;color: rgb(' +
                                             str(red) + ',' +str(green) + ',' +str(blue) + ')')
            self.radio[key].toggle()
            self.radioP[key] = QtGui.QGraphicsProxyWidget()
            self.radioP[key].setWidget(self.radio[key])
            self.dynamicWidgetsLayout.addItem(self.radioP[key], 1, i)
            i+=1
        self.dynamicWidgets.setLayout(self.dynamicWidgetsLayout)
        self.win.addItem(self.dynamicWidgets, 1, 0, 1, len(group))
        self.win.nextRow()
        self.PlotData()

    def PlotData(self):
        self.plotCanvas = QtGui.QGraphicsWidget()
        self.plotCanvasLayout = QtGui.QGraphicsGridLayout(self.plotCanvas)
        for canvas in self.plots:
            for file in self.group:
                pass