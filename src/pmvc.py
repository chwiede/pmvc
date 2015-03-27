#!/usr/bin/env python

# simple.py

# packages:
# * phonon-qt5
# * python-pyqt5
# * qt5-multimedia

import os
import sys
import time
import threading

from mainwindow import MainWindow
from PyQt5.QtWidgets import *

### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()
    
    sys.exit(app.exec_())