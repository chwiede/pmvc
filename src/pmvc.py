#!/usr/bin/env python

import os
import sys
from PyQt5.QtWidgets import QApplication
from modules.mainwindow import MainWindow
from modules.localization import localize

if __name__ == '__main__':
    # setup localization
    localize(os.path.dirname(__file__) + '/locale')

    # load app
    app = QApplication(sys.argv)

    # start app
    mainWindow = MainWindow(os.path.dirname(__file__) + '/icons')
    mainWindow.show()

    # bye bye
    sys.exit(app.exec_())