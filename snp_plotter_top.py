import numpy as np
from Tkinter import *
import os
import re
import random

#interactive plotting
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from pyqtgraph.colormap import ColorMap
import pyqtgraph.console

#my Stuff
from get_user_file_constraints import UserLimits
from charts import smith
from UI import UserInterface
from converter import convert_snp_csv


# import pdb;pdb.set_trace()

#----------User input 
root = Tk()                                               
user_input = UserInterface(master=root)    #creates instance of UI   
user_input.mainloop()                      #keeps loop open until user hits 'Go'
files =user_input.filez                    #first file set
root.destroy()                             #closes UI

#convert_data to pandas df
frames = []
order  = []
for file in files:    
    frames.append(convert_snp_csv(file))
    extension = os.path.splitext(file)[1]    
    num = [int(s) for s in re.findall(r'\d+', extension)] #get file extension
    order.append(num[0])    #get 'n' number associated with SnP  (order)
    
# get user constrains
filetype = max(order)  #finds highest order snp file
root=Tk()
user_constrainsts=UserLimits(filetype,master=root)      
user_constrainsts.mainloop()   
root.destroy()   

#necessary variable definitions
counter=0
plots  ={}
legnd  ={}
data   ={}
curves ={}

#*******************interactive plotting****************************************
app = QtGui.QApplication([])
layout = QtGui.QGridLayout()
win = pg.GraphicsWindow(title="Basic plotting examples")
win.setLayout(layout)
win.resize(1000,600)
win.setWindowTitle('Smith_Charts')
pg.setConfigOptions(antialias=True) # Enable antialiasing for prettier plots

#--add Widget---------------------------------------------------------------------





got_lr = False
for j in range (1,filetype+1):     #first integer of snp    
    for i in range (1,filetype+1): #second integer of snp            
    
        if user_constrainsts.plot[counter].get()==1: #plot true/false                                    
            
            #title is the main key for dictionaries
            if user_constrainsts.graphtype[counter].get()==1: #Magnitude title
                title = 'Magnitude_S'+str(j)+str(i)+':'                
            else: #smith chart title
                title = 'Smith_S'+str(j)+str(i)+':'
            
            plots[title]=win.addPlot(title=title,name = title)
            legnd[title] = plots[title].addLegend(size=(0.001,0.001)) 
            data[title]  =[]    
            curves[title]={}
            data[title]  ={}            
            for df in frames:    
                try:
                    name_of_curve = str(df['sourcefile'].iloc[0])+':' #for legend                                        
                    if user_constrainsts.graphtype[counter].get()==1: #dB 
                        #Plot Magnitude data
                        plots[title].plot(x=np.asarray(df['MHz']),
                                          y=np.asarray(df['S'+str(j)+str(i)+'_Mag']),
                                          pen=random.randint(0,255),
                                          row=i-1,col=j-1,
                                          name=name_of_curve)   
                        #Fill dictionary of data associated with each plot
                        data[title][name_of_curve] = df[['MHz',
                                                         'S'+str(j)+str(i)+'_Mag',
                                                         'sourcefile']]
                        plots[title].showGrid(x=True,y=True,alpha=.8)
                        
                        if got_lr == False: #if we are working on 1st Magnitude plot
                            #set limits of linearregion item to max and min of data
                            lr = pg.LinearRegionItem([np.asarray(df['MHz']).min(),
                                                      np.asarray(df['MHz']).max()])
                            lr.setZValue(-10)#???
                            plots[title].addItem(lr)#add lr object to Magnitude plot
                            got_lr = True  #Dont add more linearregion objects
                    else:                        
                        #Complex impedance = x+yi
                        x = np.asarray(df['S'+str(j)+str(i)+'R'])
                        y = np.asarray(df['S'+str(j)+str(i)+'I'])
                        #put smith chart in background
                        smith(plots[title]) 
                        #Plot Magnitude data                        
                        curves[title][name_of_curve]=plots[title].plot(x,y,
                                                       pen=random.randint(0,255),
                                                       name=name_of_curve)                                                                                
                        #Fill dictionary of data associated with each plot
                        data[title][name_of_curve] = df[['MHz',
                                                         'S'+str(j)+str(i)+'R',
                                                         'S'+str(j)+str(i)+'I',
                                                         'sourcefile']]
                except KeyError:
                    pass
        counter = counter+1
    win.nextRow()                

    






#updates the smith charts data based on virticle bars
def update():
    global curves,plots,data,ptr,lr
    min,max = lr.getRegion() #in MHz    
    for title,value in plots.iteritems():
        if 'Smith' in title:
            for curve,value1 in curves[title].iteritems():                                            
                slice = data[title][curve][(data[title][curve]['MHz']>=min) &
                               (data[title][curve]['MHz']<=max)]                                                                                                                                     
                columns = data[title][curve].columns
                x_vals  = np.asarray(slice[columns[1]])
                y_vals  = np.asarray(slice[columns[2]])                
                curves[title][curve].setData(x=x_vals,y=y_vals)                                                                                     

#if there is at least one Magnitude plot than there is a virticle bar
if got_lr == True:
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(50)

#links mouse position to data information (in window title)
def mouseMoved(evt):
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    for plot,value in plots.iteritems():
        vb = value.vb
        if plots[plot].sceneBoundingRect().contains(pos):
            mousePoint = vb.mapSceneToView(pos)            
            data_pointx = mousePoint.x()
            data_pointy = mousePoint.y()              
            
            
            if 'Smith' in plot:  #if mouse in smith chart calculate smith data
                complex = np.complex(data_pointx+data_pointy*1j)                
                gamma = np.sqrt(np.square(np.real(complex))+\
                        np.square(np.imag(complex))) 
                vswr = (1+gamma)/(1-gamma)
                returnloss = -20*np.log10(gamma)
                
                data_string = ' Impedance: ' + str(round(np.real(complex),2))+\
                              '+'+str(round(np.imag(complex),2))+'j'+\
                              ' VSWR: '+str(round(vswr,3))+\
                              ' ReturnLoss: '+str(round(returnloss,2))                
            
            else: #if mouse in Magnitude plot return Freq & magnitude in dBm
                data_string='('+str(round(data_pointx,3))+'MHz'+\
                            ' ,'+str(round(data_pointy,3))+'dBm)'                        
            # label.setText(data_string)
            win.setWindowTitle('SnP_Plots: '+data_string)
    
for plot,value in plots.iteritems(): #link mosuse to function for each plot
    proxy = pg.SignalProxy(value.scene().sigMouseMoved,
                           rateLimit=60,
                           slot=mouseMoved)    
        
print pg.GraphicsLayout()  
 
'''Main Loop'''
## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        
        
     