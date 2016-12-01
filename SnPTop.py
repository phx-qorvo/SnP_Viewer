from MainWindow import SnpPlotter
from pyqtgraph.Qt import QtGui, QtCore
import sip

Plotter = SnpPlotter()

'''Main Loop'''
# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        sip.setdestroyonexit(False)
        QtGui.QApplication.instance().exec_()
