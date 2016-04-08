import skrf as rf
import pylab
from pylab import *
import numpy as np
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
import csv
import os

from UI_file_select import UserInterface
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import ctypes
from scipy.sparse.csgraph import _validation

from distutils.core import setup
import py2exe





includes =['matplotlib','pytz', 'scipy.special._ufuncs_cxx','scipy.sparse.csgraph._validation','sip']

setup(console=["snp_plotter_top.py"],      
      options={
               'py2exe': {
                          'packages' :  includes,                          
                          'excludes' :  'proxy_base.py',
                          'dll_excludes': ['libgdk-win32-2.0-0.dll',
                                         'libgobject-2.0-0.dll',
                                         'libgdk_pixbuf-2.0-0.dll',
                                         'libgtk-win32-2.0-0.dll',
                                         'libglib-2.0-0.dll',
                                         'libcairo-2.dll',
                                         'libpango-1.0-0.dll',
                                         'libpangowin32-1.0-0.dll',
                                         'libpangocairo-1.0-0.dll',
                                         'libglade-2.0-0.dll',
                                         'libgmodule-2.0-0.dll',
                                         'libgthread-2.0-0.dll',
                                         'QtGui4.dll', 'QtCore.dll',
                                         'QtCore4.dll'
                                        ],
                          }
                },
      data_files=['C:\Users\rt867573\AppData\Local\Continuum\Anaconda\tcl\tcl8.5\init.tcl'],)   #matplotlib.get_py2exe_datafiles(),


