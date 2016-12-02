from MainWindow import SnpPlotter
from pyqtgraph.Qt import QtGui, QtCore
import sip

Plotter = SnpPlotter()

#
# Notes:
# 1. Select new data -  Done
# 2. checkbox filenames (wrap em)
#     3. Run plot selection by itself with existing data
#     4. marker information window
#     5. windowing multiple regions
#     6. multiple charts of same port logmag
#     7. save and recall template
#

'''Main Loop'''
# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        sip.setdestroyonexit(False)
        QtGui.QApplication.instance().exec_()
