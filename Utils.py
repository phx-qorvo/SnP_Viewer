import numpy as np
import pyqtgraph as pg
from read_touchstone import Touchstone
import pandas as pd
import numpy as np
import os
import re


def convert_snp_csv(file):
    Instance = Touchstone(file)
    freq, array = Instance.get_sparameter_arrays()
    names = Instance.get_sparameter_names()
    sParams = pd.DataFrame(columns=names)
    for i, name in enumerate(names):
        if i == 0:
            sParams[str(name)] = freq
        else:
            # S11 is indexs 00 and s21 is indexs 10 etc..
            if 'R' in name:
                sParams[name] = np.real(
                    array[:, int(name[1]) - 1, int(name[2]) - 1])
            if 'I' in name:
                sParams[name] = np.imag(
                    array[:, int(name[1]) - 1, int(name[2]) - 1])
    head, tail = os.path.split(file)
    filename, file_extension = os.path.splitext(tail)
    # calculate mag_phase (goes up to 20 port, but can easily add more)
    for x in range(0, 20):
        for y in range(0, 20):
            if 'S' + str(x) + str(y) + 'R' in sParams.columns:
                complex = sParams['S' + str(x) + str(y) + 'R'] + \
                          sParams['S' + str(x) + str(y) + 'I'] * 1j

                sParams['S' + str(x) + str(y) + '_dB'] = 20 * np.log10(
                    np.absolute(complex))

                sParams['S' + str(x) + str(y) + '_Ang'] = np.angle(complex, deg=True)
    # More Calculated columns
    sParams['sourcefile'] = filename
    sParams['Frequency'] = sParams['frequency'] * (1 / 1e6)
    sParams = sParams.drop('frequency', 1)
    num = [int(s) for s in re.findall(r'\d+', file_extension)]  # get file extension
    sParams['order'] = num[0]
    #move Frequency to be the first column
    columns = list(sParams.columns.values)
    columns.insert(0,columns.pop(columns.index('Frequency')))
    sParams = sParams[columns]
    return sParams


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