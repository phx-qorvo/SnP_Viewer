from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import tkinter
from tkinter import *

def smith(p,white_backgorund):
    # make smith Chart
    p.setAspectLocked()
    p.setXRange(-1, 1, padding=0)
    p.setYRange(-1, 1, padding=0)

    if white_backgorund:
            pen1 = 'k'
            pen2 = 'b'
    else:
            pen1 = 'w'
            pen2 = 'g'

    rline = [0.2, 0.5, 1.0, 2.0, 5.0]
    xline = [0.2, 0.5, 1, 2, 5]

    # plot perimiter unit circle in white
    circle1 = pg.QtGui.QGraphicsEllipseItem(1, -1, -2, 2)
    circle1.setPen(pg.mkPen(pen1, width=0))
    circle1.setFlag(circle1.ItemClipsChildrenToShape)
    p.addItem(circle1)

    # plot real,imaginary axis in white
    p.plot(x=np.asarray([0,0]),y=np.asarray([-1,1]),pen=pen1)
    p.plot(x=np.asarray([-1,1]),y=np.asarray([0,0]),pen=pen1)
    
    pathItem = pg.QtGui.QGraphicsPathItem()
    path = pg.QtGui.QPainterPath()
    path.moveTo(1, 0)
    
    # plot ellipsies in green
    for r in rline:
        raggio = 1./(1+r)
        path.addEllipse(1, -raggio, -raggio*2, raggio*2)
    
    for x in xline:
        path.arcTo(x + 1, 0, -x*2, x*2, 90, -180)
        path.moveTo(1, 0)
        path.arcTo(x + 1, 0, -x*2, -x*2, 270, 180)    
        
    pathItem.setPath(path)
    pathItem.setPen(pg.mkPen(pen2, width = 0.2))
    pathItem.setParentItem(circle1)


#below is code filled into the 'pre-canned' python scripts
moving_average = \
'''# --------------------moving average: ---------------------------------------
import pandas as pd; import numpy as np
ewma = pd.stats.moments.ewma

#Edit wich data set  (Replace 'A' with your trace)
df = data['A'][(data['A']['MHz']>0) & (data['A']['MHz']<12000)]

y =np.asarray( df['S12_Mag']); x=np.asarray(df['MHz'])

# take EWMA in both directions with a smaller span term
fwd = ewma( y, span=15 ) # take EWMA in fwd direction
bwd = ewma( y[::-1], span=15 ) # take EWMA in bwd direction
ma = np.vstack(( fwd, bwd[::-1] )) # lump fwd and bwd together
ma = np.mean( ma, axis=0 ) # average

#EDIT WHICH PLOT YOU WANT THIS ON (Replace 'dB_S12' with the plot you want this on)
plots['dB_S12'].addLegend(size = (0.001,0.001))
plots['dB_S12'].plot(x=x,y=ma,pen=91,name = 'MovingAvg')
'''
power_gain = \
'''# --------------------------Power Gain---------------------------------------
import numpy as np; import pandas as pd

#Edit wich data set  (Replace 'A' with your trace)
df = data['A'][(data['A']['MHz']>0) & (data['A']['MHz']<12000)]

s11_complex 		= np.vectorize(complex)(df['S11R'],df['S11I'])
s22_complex		= np.vectorize(complex)(df['S22R'],df['S22I'])
s21_complex		= np.vectorize(complex)(df['S21R'],df['S21I'])
s12_complex		= np.vectorize(complex)(df['S12R'],df['S12I'])

Power_Gain      = 10*np.log(np.absolute(s21_complex)**2/(1-(np.absolute(s11_complex)**2)))
x=np.asarray(df['MHz']); y = Power_Gain
#EDIT WHICH PLOT YOU WANT THIS ON (Replace 'dB_S12' with the plot you want this on)
plots['dB_S12'].addLegend(size = (0.001,0.001))
plots['dB_S12'].plot(x=x,y=y,pen=91,name = 'PowerGain')

'''
vswr_circles =\
'''# --------------------------VSWR Circles---------------------------------------
import numpy as np; import pandas as pd;from pyqtgraph.Qt import QtGui, QtCore

vswr = 3.0

mag_gamma=(vswr-1)/(vswr+1)
phase=np.linspace(-np.pi,np.pi,100)
gamma = 1j*phase
gamma_complex = mag_gamma*np.exp(gamma)

plots['Smith_S11'].plot(x=gamma_complex.real,y=gamma_complex.imag,pen={'color': (255,0,0), 'width': 3,'style':QtCore.Qt.DotLine})
'''
spec_lines =\
'''# --------------------------    Spec Lines     ---------------------------------------
import numpy as np; import pandas as pd;from pyqtgraph.Qt import QtGui, QtCore

x=np.asarray([1000,2000])       #X-Limits
y=np.asarray([-10,-10])         #Y-Limits

plots['dB_S12'].plot(x=x,y=y,pen={'color': (255,0,0), 'width': 3,'style':QtCore.Qt.DotLine})

'''