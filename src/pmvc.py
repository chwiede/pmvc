#!/usr/bin/env python

import os
import sys
from PyQt5.QtWidgets import QApplication
from modules.mainwindow import MainWindow
from modules.localization import localize

if __name__ == '__main__':
    # setup localization
    localize('./locale')

    # load app
    app = QApplication(sys.argv)

    # start app
    mainWindow = MainWindow(os.path.abspath('icons'))
    mainWindow.show()

    # bye bye
    sys.exit(app.exec_())