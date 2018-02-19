#!/usr/bin/env python

import os
import sys
from PyQt5.QtWidgets import QApplication
from modules.mainwindow import MainWindow
from modules.localization import localize

if __name__ == '__main__':
    # setup localization
    locale_path = os.path.join(os.path.dirname(__file__), 'locale')
    print("loading locale from %s..." % locale_path)
    localize(locale_path)

    # load app
    app = QApplication(sys.argv)

    # start app
    icons_path = os.path.join(os.path.dirname(__file__), 'icons')
    print("loading icons from %s..." % icons_path)
    mainWindow = MainWindow(icons_path)
    mainWindow.show()

    # bye bye
    sys.exit(app.exec_())
