#!/usr/bin/env python

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class CutWidget(QWidget):
  
    def __init__(self, parent = None):      
        super(CutWidget, self).__init__(parent)        
        self.initUI()
        
        
    def initUI(self):
        print("INIT CUTWIDG")        
        self.setMinimumSize(100, 15)
        self.setMaximumHeight(32)
        self.Duration = 0
        self.Cuts = []
        self.Position = 0



    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()
      
      
    def drawWidget(self, qp):
        size = self.size()
        w = size.width()-1
        h = size.height()-1
        
        # background
        qp.setPen(QColor(96, 96, 96))
        qp.setBrush(QColor(64, 128, 48))
        qp.drawRect(0, 0, w, h)
        
        # draw cut areas
        if self.Cuts != None and len(self.Cuts) > 0:
            last = 0.0
            doCut = True
            qp.setPen(Qt.transparent)
            qp.setBrush(QColor(196, 48, 16))
            for cut in self.Cuts + [self.Duration]:
                
                if doCut and self.Duration > 0:
                    x1 = (w / self.Duration) * last
                    x2 = (w / self.Duration) * cut
                    qp.drawRect(x1, 1, x2-x1+1, h-1)                                
                
                last = cut
                doCut = not doCut

        # draw position marker & time
        if self.Duration > 0:
            qp.setPen(Qt.transparent)
            qp.setBrush(QColor(16, 16, 16))
            x = (w / self.Duration) * self.Position
            points = [QPoint(x-5, 1), QPoint(x, 6), QPoint(x+5, 1)]
            triangle = QPolygon(points)
            qp.drawPolygon(triangle)        
            points = [QPoint(x-5, h), QPoint(x, h-6), QPoint(x+5, h)]
            triangle = QPolygon(points)
            qp.drawPolygon(triangle)
        
    
    def clear(self):
        self.Cuts.clear()
        self.update()
            
            
    def setPosition(self, position):
        self.Position = position
        self.update()
        
    
    def setDuration(self, milliseconds):
        self.Duration = milliseconds
        self.update()
        
        
    def deleteCut(self, millisecond):
        self.Cuts.remove(millisecond)
        self.update()


    def addCut(self, millisecond):
        # check if position already in list!?
        if self.Cuts != None and len(self.Cuts) > 0:
            closest = sorted(self.Cuts, key = lambda c: abs(c-millisecond))[0]
            if abs(closest - millisecond) < 240:
                return
            
        
        self.Cuts.append(millisecond)
        self.Cuts.sort()        
        self.update()
        
        