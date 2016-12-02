import numpy as np
import pyqtgraph as pg
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