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
from Utils import smith
from convert_snp_to_pandas_df import convert_snp_csv



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
        # Dictionaries to keep track of dynamic widgets
        self.files = {}
        self.filesP = {}
        self.markerFreq={}
        self.markerFreqP={}
        self.freqSlice = {}
        self.freqSlice = {}
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
        self.numberOfWindows.textChanged.connect(self.ValidateWindowCount)
        self.numberOfWindows.setStyleSheet('background-color:black;border-style: outset;color: rgb(255,255,255)')
        self.numberOfWindows.setPlaceholderText("How Many Data Windows")
        self.numberOfWindowsP = QtGui.QGraphicsProxyWidget()
        self.numberOfWindowsP.setWidget(self.numberOfWindows)
        self.staticLayout.addItem(self.numberOfWindowsP, 0, 1)
        self.staticWidgets.setLayout(self.staticLayout)
        self.win.addItem(self.staticWidgets, 0, 0, 1, 1)

    def GrabData(self):
        root = Tk()
        root.withdraw()
        files = tkinter.filedialog.askopenfilenames(title='Choose Set of files')
        root.destroy()
        frames = []
        self.df = pd.DataFrame
        for f in files:
            frames.append(convert_snp_csv(f))
        self.df = pd.concat(frames)
        self.group = self.df.groupby('sourcefile')
        self.ValidateFiles()

    def ValidateWindowCount(self):
        self.windowCount = self.doubleValidator.validate(self.numberOfWindows.text(), 0)[1]
        if self.windowCount != '' and not self.df.empty and not bool(self.titles): #if they have never been created
            self.PopulateFilesWidgets()
            self.windowControlWidgets()
        elif self.windowCount != '' and not self.df.empty and bool(self.titles): #if we have already created them once
            self.windowControlWidgets()
        else: # criteria not met (need both files and number of windows to start)
            pass

    def ValidateFiles(self):
        self.windowCount = self.doubleValidator.validate(self.numberOfWindows.text(), 0)[1]
        if self.windowCount != '' and not self.df.empty  and not bool(self.titles): #if they have never been created
            self.PopulateFilesWidgets()
            self.windowControlWidgets()
        elif self.windowCount != '' and not self.df.empty and bool(self.titles): #if we have already created them once
            self.PopulateFilesWidgets()
            self.PlotData()
        else: # criteria not met (need both files and number of windows to start)
            pass

    def PopulateFilesWidgets(self):
        self.filesWidgets = QtGui.QGraphicsWidget()
        self.filesWidgetsLayout = QtGui.QGraphicsGridLayout(self.filesWidgets)
        self.files={}
        self.filesP={}
        self.dynamicRows=1
        #Files Label
        self.filesLabel = QtGui.QLineEdit()
        self.filesLabel.setText("------------------------------Files--------------------------------------")
        self.filesLabel.isReadOnly()
        self.filesLabel.setStyleSheet(
            'font: bold 14px;background-color:black;border-style: outset;color: rgb(255,255,255)')
        self.filesLabelP = QtGui.QGraphicsProxyWidget()
        self.filesLabelP.setWidget(self.filesLabel)
        self.filesWidgetsLayout.addItem(self.filesLabelP, 0, 0, 1, 15)

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
            self.files[file].stateChanged.connect(self.CreateCanvases)
            self.filesP[file] = QtGui.QGraphicsProxyWidget()
            self.filesP[file].setWidget(self.files[file])
            if column > 6:
                self.dynamicRows += 1
                column = 0
            self.filesWidgetsLayout.addItem(self.filesP[file], self.dynamicRows, column)
            column += 1
        # add widgets do dynamic Layout
        self.dynamicRows += 1
        self.filesWidgets.setLayout(self.filesWidgetsLayout)
        self.win.addItem(self.filesWidgets, 0, 1)

    def windowControlWidgets(self):
        self.dynamicWidgets = QtGui.QGraphicsWidget()
        self.dynamicWidgetsLayout = QtGui.QGraphicsGridLayout(self.dynamicWidgets)
        self.titles={}
        self.titlesP={}
        self.markerFreq={}
        self.markerFreqP={}
        self.freqSlice={}
        self.freqSliceP={}
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
        self.dynamicWidgetsLayout.addItem(self.filesLabel, 0, 0, 1, 5)
        row = 1
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
            self.dynamicWidgetsLayout.addItem(self.titlesP[window], row, 0)
            # Smith OR LogMag Plot type
            self.smithBoxes[window] = QtGui.QCheckBox('Smith')
            self.smithBoxes[window].setStyleSheet('background-color:black;'
                                                 'border-style: outset;'
                                                 'color: rgb(255,255,255)')
            self.smithBoxes[window].stateChanged.connect(self.CreateCanvases)
            self.smithBoxesP[window] = QtGui.QGraphicsProxyWidget()
            self.smithBoxesP[window].setWidget(self.smithBoxes[window])
            self.dynamicWidgetsLayout.addItem(self.smithBoxesP[window], row, 1)
            self.logMagBoxes[window] = QtGui.QCheckBox("logMag")
            self.logMagBoxes[window].setStyleSheet('background-color:black;'
                                                 'border-style: outset;'
                                                 'color: rgb(255,255,255)')
            self.logMagBoxes[window].stateChanged.connect(self.CreateCanvases)
            self.logMagBoxesP[window] = QtGui.QGraphicsProxyWidget()
            self.logMagBoxesP[window].setWidget(self.logMagBoxes[window])
            self.dynamicWidgetsLayout.addItem(self.logMagBoxesP[window], row, 2)
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
            self.dynamicWidgetsLayout.addItem(self.markerFreqP[window], row,3)
            # Frequency Window
            self.freqSlice[window] = QtGui.QLineEdit()
            self.freqSlice[window].setStyleSheet('background-color: black;'
                                                  'border-width: 1px;'
                                                  'border-color: #339;'
                                                  'border-style: solid;'
                                                  'border-radius: 7;'
                                                  'padding: 3px;'
                                                  'min-width: 150px;'
                                                  'max-width: 250px;'
                                                  'color: rgb(255,255,255)')

            self.freqSlice[window].setPlaceholderText("Freq Window Ex(740:1000,1200:1340)")
            self.freqSliceP[window] = QtGui.QGraphicsProxyWidget()
            self.freqSliceP[window].setWidget(self.freqSlice[window])
            self.dynamicWidgetsLayout.addItem(self.freqSliceP[window], row, 4)
            # populate port choices
            self.ports[window] = {}
            self.portsP[window] = {}
            column=5
            for x in range(1,self.df.order.max()+1):
                for y in range(1,self.df.order.max()+1):
                    self.ports[window]['S{}{}'.format(x,y)]=QtGui.QCheckBox('{}{}'.format(x,y))
                    self.ports[window]['S{}{}'.format(x, y)].stateChanged.connect(self.CreateCanvases)
                    self.ports[window]['S{}{}'.format(x, y)].setStyleSheet('background-color:black;'
                                                                                     'border-style: outset;'
                                                                                     'color: rgb(255,255,255)')
                    self.portsP[window]['S{}{}'.format(x,y)] = QtGui.QGraphicsProxyWidget()
                    self.portsP[window]['S{}{}'.format(x, y)].\
                        setWidget(self.ports[window]['S{}{}'.format(x,y)])
                    self.dynamicWidgetsLayout.addItem(self.portsP[window]['S{}{}'.format(x, y)],
                                                      row, column)
                    column += 1
            row += 1
        # Add widgets to Layout
        self.dynamicWidgets.setLayout(self.dynamicWidgetsLayout)
        self.win.addItem(self.dynamicWidgets, 1, 0, 1, 2)
        self.CreateCanvases()

    def CreateCanvases(self):
        self.canvas = {}
        self.plotCanvas = QtGui.QGraphicsWidget()
        self.plotCanvasLayout = QtGui.QGraphicsGridLayout(self.plotCanvas)
        columns = int(np.ceil(np.sqrt(int(self.windowCount))))
        row=0
        col=0
        for window in range(0,int(self.windowCount)):
            window=str(window)
            if col == columns:
                row += 1
                col=0
            self.canvas[window] = pg.PlotItem(title=str(self.titles[window].text()))
            self.plotCanvasLayout.addItem(self.canvas[window],row,col)
            col += 1
        self.plotCanvas.setLayout(self.plotCanvasLayout)
        self.win.addItem(self.plotCanvas, 2, 0, 1, 2)
        self.PlotData()

    def PlotData(self):
        self.traces ={}
        for window, canvas in self.canvas.items(): # on each plot
            self.traces[window]={}
            for file, g in self.group:         # Every file
                dataSections = [g]
                freqSections = 'full'
                if self.freqSlice[window].text() !='':
                    dataSections=[]
                    freqSections = self.freqSlice[window].text().replace(':','<=Frequency<=').split(',')
                    for s in freqSections:
                        dataSections.append(g.query(s))
                for data,section in zip(dataSections,freqSections):
                    if self.files[file].isChecked():
                        for portKey, port in self.ports[window].items():  #Every Port
                            if self.smithBoxes[window].isChecked() and port.isChecked():
                                smith(p=self.canvas[window],white_backgorund=False)
                                print('{}{}{}'.format(file,portKey,section))
                                self.traces[window]['{}{}{}'.format(file,portKey,section)]=\
                                    self.canvas[window].plot(x=np.asarray(data[portKey + 'R']),
                                                             y=np.asarray(data[portKey + 'I']),
                                                             pen=self.colors[file])
                            elif port.isChecked(): #LogMag
                                self.traces[window]['{}{}'.format(file,portKey,section)] = \
                                    self.canvas[window].plot(x=np.asarray(data.Frequency),
                                                             y=np.asarray(data[portKey+'_dB']),
                                                             pen=self.colors[file])
                            else: # Not a chosen port
                                pass
                    else:   # Not a chosen File
                        pass