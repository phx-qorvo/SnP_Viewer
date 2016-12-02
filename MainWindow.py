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
        self.staticLayout = QtGui.QGridLayout()
        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.win.setLayout(self.staticLayout)
        self.win.resize(1000, 600)
        self.win.setWindowTitle('Smith_Charts')
        pg.setConfigOptions(antialias=True)  # Enable anti-aliasing for prettier plots
        # ******************  Variable Definitions ***********************************
        self.df = pd.DataFrame  # where main bulk of data is stored
        self.windowCount = 1
        # ********************** Dynamic widgets decelerations ****************************************

        self.plotTypeGroup = {}
        self.plotCanvas = QtGui.QGraphicsWidget()
        self.plotCanvasLayout = QtGui.QGraphicsGridLayout(self.plotCanvas)
        self.filesLabel = QtGui.QLabel()
        # Dictionaries to keep track of user settings
        self.settings={}
        self.currentSelectedWindow = 0
        self.order=0
        # Dictionaries to keep track of dynamic widgets
        self.files = {}
        self.filesP = {}
        self.markerFreq={}
        self.markerFreqP={}
        self.freqWindow = {}
        self.freqWindow = {}
        self.colors = {}
        self.canvas = {}
        self.titles={}
        self.titlesP={}
        self.smithBoxes={}
        self.smithBoxesP ={}
        self.logMagBoxes={}
        self.logMagBoxesP={}
        self.plots = {}
        self.trace = {}
        self.ports = {}
        self.portsP = {}
        self.dynamicRows=1
        # ******************** Static widgets *****************************************************
        self.staticWidgets = QtGui.QGraphicsWidget()
        self.staticLayout = QtGui.QGraphicsGridLayout(self.staticWidgets)
        # Data selection button
        self.dataButton = QtGui.QPushButton('Grab Data')
        self.dataButtonP = QtGui.QGraphicsProxyWidget()
        self.dataButtonP.setWidget(self.dataButton)
        self.dataButton.clicked.connect(self.GrabData)
        self.staticLayout.addItem(self.dataButtonP, 0, 0)
        # Number of windows
        self.numberOfWindows = QtGui.QLineEdit()
        self.doubleValidator = QtGui.QIntValidator()
        self.numberOfWindows.setValidator(self.doubleValidator)
        self.numberOfWindows.textChanged.connect(self.ValidateInput)
        self.numberOfWindows.setStyleSheet('background-color:black;border-style: outset;color: rgb(255,255,255)')
        self.numberOfWindows.setPlaceholderText("How Many Data Windows")
        self.numberOfWindowsP = QtGui.QGraphicsProxyWidget()
        self.numberOfWindowsP.setWidget(self.numberOfWindows)
        self.staticLayout.addItem(self.numberOfWindowsP, 0, 1)
        self.staticWidgets.setLayout(self.staticLayout)
        self.win.addItem(self.staticWidgets, 0, 0, 1, 1)
        self.win.nextRow()

    def GrabData(self):
        root = Tk()
        root.withdraw()
        files = tkinter.filedialog.askopenfilenames(title='Choose Set of files')
        root.destroy()
        frames = []
        for f in files:
            frames.append(convert_snp_csv(f))
        self.df = pd.concat(frames)
        self.order = self.df.order.max()
        print(self.order)
        self.group = self.df.groupby('sourcefile')
        self.ValidateInput()

    def ValidateInput(self):
        #Cant procede without touchstone files AND number of windows to generate
        self.windowCount = self.doubleValidator.validate(self.numberOfWindows.text(), 0)[1]
        if self.windowCount != '' and self.order !=0:
            self.PopulateFilesWidgets()
        else:
            pass


    def PopulateFilesWidgets(self):
        self.dynamicWidgets = QtGui.QGraphicsWidget()
        self.dynamicWidgetsLayout = QtGui.QGraphicsGridLayout(self.dynamicWidgets)
        self.files={}
        self.filesP={}
        self.ports={}
        self.portsP={}
        self.dynamicRows=1
        #Files Label
        self.filesLabel = QtGui.QLineEdit()
        self.filesLabel.setText("------------------------------Files--------------------------------------")
        self.filesLabel.isReadOnly()
        self.filesLabel.setStyleSheet(
            'font: bold 14px;background-color:black;border-style: outset;color: rgb(255,255,255)')
        self.filesLabelP = QtGui.QGraphicsProxyWidget()
        self.filesLabelP.setWidget(self.filesLabel)
        self.dynamicWidgetsLayout.addItem(self.filesLabelP, 0, 0, 1, 5)

        colorMap = iter(cm.gist_rainbow(np.linspace(0, 1, len(self.group))))
        column = 0
        for file, g in self.group:
            red, green, blue, a = next(colorMap)
            red = int(red * 255)
            green = int(green * 255)
            blue = int(blue * 255)
            self.colors[file] = QtGui.QColor(red, green, blue)
            # selectable files
            self.files[file] = QtGui.QCheckBox(file[-30:])
            self.files[file].setStyleSheet('background-color:black;'
                                           'border-style: outset;'
                                           'color: rgb({},{},{})'.format(red,green,blue))
            self.files[file].toggle()
            self.filesP[file] = QtGui.QGraphicsProxyWidget()
            self.filesP[file].setWidget(self.files[file])
            if column > 4:
                self.dynamicRows += 1
                column = 0
            self.dynamicWidgetsLayout.addItem(self.filesP[file], self.dynamicRows, column)
            column += 1
        # add widgets do dynamic Layout
        self.dynamicRows += 1
        self.dynamicWidgets.setLayout(self.dynamicWidgetsLayout)
        self.win.addItem(self.dynamicWidgets, 1, 0)
        self.windowControlWidgets()

    def windowControlWidgets(self):
        self.titles={}
        self.titlesP={}
        self.markerFreq={}
        self.markerFreqP={}
        self.freqWindow={}
        self.freqWindowP={}
        self.smithBoxes={}
        self.smithBoxesP={}
        self.logMagBoxes={}
        self.logMagBoxesP={}
        self.plotTypeGroup={}
        # Window control Label
        self.windowControls = QtGui.QLineEdit()
        self.windowControls.setText("------------------------------Window Controls--------------------------------------")
        self.windowControls.isReadOnly()
        self.windowControls.setStyleSheet('font: bold 14px;'
                                          'background-color:black;'
                                          'border-style:'
                                          'outset;color: rgb(255,255,255)')
        self.filesLabel = QtGui.QGraphicsProxyWidget()
        self.filesLabel.setWidget(self.windowControls)
        self.dynamicWidgetsLayout.addItem(self.filesLabel, self.dynamicRows, 0, 1, 5)
        self.dynamicRows += 1

        for window in range(0,int(self.windowCount)):
            window = str(window)
            # Editable Titles
            self.titles[window] = QtGui.QLineEdit()
            self.titles[window].setStyleSheet('background-color: black;'
                                                  'border-width: 1px;'
                                                  'border-color: #339;'
                                                  'border-style: solid;'
                                                  'border-radius: 7;'
                                                  'padding: 3px;'
                                                  'min-width: 150px;'
                                                  'max-width: 250px;'
                                                  'color: rgb(255,255,255)')
            self.titles[window].setPlaceholderText("Window {} Title".format(window))
            self.titles[window].textChanged.connect(self.CreateCanvases)
            self.titlesP[window] = QtGui.QGraphicsProxyWidget()
            self.titlesP[window].setWidget(self.titles[window])
            self.dynamicWidgetsLayout.addItem(self.titlesP[window], self.dynamicRows, 0)
            # Smith OR LogMag Plot type
            self.smithBoxes[window] = QtGui.QCheckBox('Smith')
            self.smithBoxes[window].setStyleSheet('background-color:black;'
                                                 'border-style: outset;'
                                                 'color: rgb(255,255,255)')
            self.smithBoxesP[window] = QtGui.QGraphicsProxyWidget()
            self.smithBoxesP[window].setWidget(self.smithBoxes[window])
            self.dynamicWidgetsLayout.addItem(self.smithBoxesP[window], self.dynamicRows, 1)
            self.logMagBoxes[window] = QtGui.QCheckBox("logMag")
            self.logMagBoxes[window].setStyleSheet('background-color:black;'
                                                 'border-style: outset;'
                                                 'color: rgb(255,255,255)')
            self.logMagBoxesP[window] = QtGui.QGraphicsProxyWidget()
            self.logMagBoxesP[window].setWidget(self.logMagBoxes[window])
            self.dynamicWidgetsLayout.addItem(self.logMagBoxesP[window], self.dynamicRows, 2)
            # Make plot types mutually exclusive
            self.plotTypeGroup[window]= QtGui.QButtonGroup()
            self.plotTypeGroup[window].addButton(self.logMagBoxes[window])
            self.plotTypeGroup[window].addButton(self.smithBoxes[window])


            # Marker Entry
            self.markerFreq[window] = QtGui.QLineEdit()
            self.markerFreq[window].setStyleSheet('background-color: black;'
                                                  'border-width: 1px;'
                                                  'border-color: #339;'
                                                  'border-style: solid;'
                                                  'border-radius: 7;'
                                                  'padding: 3px;'
                                                  'min-width: 150px;'
                                                  'max-width: 250px;'
                                                  'color: rgb(255,255,255)')
            self.markerFreq[window].setPlaceholderText("Freq Markers Ex(740,815.3,1100)")
            self.markerFreqP[window] = QtGui.QGraphicsProxyWidget()
            self.markerFreqP[window].setWidget(self.markerFreq[window])
            self.dynamicWidgetsLayout.addItem(self.markerFreqP[window], self.dynamicRows,3)
            # Frequency Window
            self.freqWindow[window] = QtGui.QLineEdit()
            self.freqWindow[window].setStyleSheet('background-color: black;'
                                                  'border-width: 1px;'
                                                  'border-color: #339;'
                                                  'border-style: solid;'
                                                  'border-radius: 7;'
                                                  'padding: 3px;'
                                                  'min-width: 150px;'
                                                  'max-width: 250px;'
                                                  'color: rgb(255,255,255)')

            self.freqWindow[window].setPlaceholderText("Freq Window Ex(740:1000,1200:1340)")
            self.freqWindowP[window] = QtGui.QGraphicsProxyWidget()
            self.freqWindowP[window].setWidget(self.freqWindow[window])
            self.dynamicWidgetsLayout.addItem(self.freqWindowP[window],self.dynamicRows,4)
            # populate port choices
            column=5
            for x in range(1,self.order+1):
                for y in range(1,self.order+1):
                    self.ports['window_{}_S{}{}'.format(window,x,y)]=QtGui.QCheckBox('{}{}'.format(x,y))
                    self.ports['window_{}_S{}{}'.format(window, x, y)].setStyleSheet('background-color:black;'
                                                                                     'border-style: outset;'
                                                                                     'color: rgb(255,255,255)')
                    self.portsP['window_{}_S{}{}'.format(window,x,y)] = QtGui.QGraphicsProxyWidget()
                    self.portsP['window_{}_S{}{}'.format(window, x, y)].setWidget(self.ports['window_{}_S{}{}'.format(window,x,y)])
                    self.dynamicWidgetsLayout.addItem(self.portsP['window_{}_S{}{}'.format(window, x, y)],
                                                      self.dynamicRows, column)
                    column += 1
            self.dynamicRows += 1
        # Add widgets to Layout
        self.dynamicWidgets.setLayout(self.dynamicWidgetsLayout)
        self.win.addItem(self.dynamicWidgets, 1, 0)
        self.win.nextRow()
        self.CreateCanvases()

    def CreateCanvases(self):
        self.canvas = {}
        self.plotCanvas = QtGui.QGraphicsWidget()
        self.plotCanvasLayout = QtGui.QGraphicsGridLayout(self.plotCanvas)
        col = 0
        for i in range(0,int(self.windowCount)):
            window = str(i)
            if (i % self.order) == 0 and i != 0: col += 1
            row = i % self.order
            self.canvas[window] = pg.PlotItem(title=str(self.titles[window].text()))
            self.plotCanvasLayout.addItem(self.canvas[window],col,row)
        self.plotCanvas.setLayout(self.plotCanvasLayout)
        self.win.addItem(self.plotCanvas,2,0)
