from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class DumbSlider(QSlider):

    def __init__(self, parent=None):
        super(QSlider, self).__init__(parent)

    #range_changed = pyqtSignal(int, int, name='rangeChanged')
    keyPressed = pyqtSignal(QKeyEvent)

    def keyPressEvent(self, event):
        self.keyPressed.emit(event)
