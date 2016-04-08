# editor.py

from PyQt4 import QtGui
import py_syntax_highlighting

app = QtGui.QApplication([])
editor = QtGui.QPlainTextEdit()
highlight = py_syntax_highlighting.PythonHighlighter(editor.document())
editor.show()

# Load py_syntax_highlighting.py into the editor for demo purposes
infile = open('py_syntax_highlighting.py', 'r')
editor.setPlainText(infile.read())

app.exec_()