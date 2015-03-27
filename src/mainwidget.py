#!/usr/bin/env python

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import QVideoWidget

from videowidget import VideoWidget
from cutwidget import CutWidget

### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

class dumbSlider(QSlider):
    
    def __init__(self, parent=None):
        super(QSlider, self).__init__(parent)
    
    #range_changed = pyqtSignal(int, int, name='rangeChanged')
    keyPressed = pyqtSignal(QKeyEvent)
    
    def keyPressEvent(self, event):
        self.keyPressed.emit(event)
    

### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


class MainWidget(QWidget):
    
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.parent = parent
        self.InitUI()
        self.cutInProgress = False
    
    
    def InitUI(self):
        # Layout
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        # VideoWidget & player
        self.videoWidget = VideoWidget()        
        self.grid.addWidget(self.videoWidget, 0, 0, 1, 7)
        self.createPlayer()
        
        # Slider
        self.slider = dumbSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.seek)
        self.slider.keyPressed.connect(self.keyPressEvent)
        self.grid.addWidget(self.slider, 2, 3)
        
        # Buttons
        self.createButtons()
        
        # Cut Widget
        self.cutWidget = CutWidget(self)
        self.grid.addWidget(self.cutWidget, 1, 3)
        
        # Cut Listbox
        self.cutList = QComboBox(self)
        self.cutList.currentIndexChanged.connect(self.cutListSelectionChanged)
        self.grid.addWidget(self.cutList, 1, 4, 1, 3)
        
        # Time Label
        self.timeLabel = QLabel(self)
        
        f = QFont()
        f.setBold(True)
        self.timeLabel.setFont(f)        
        self.timeLabel.setText("00:00:00.00")
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.timeLabel, 1, 0, 1, 3)
        
        

    def Open(self, file):
        url = QUrl.fromLocalFile(file)
        mediacnt = QMediaContent(url)
        self.player.setMedia(mediacnt)
        self.player.play()
        self.player.pause()
        
        self.cutWidget.clear()
        self.cutList.clear()      
    
    
    
    def keyPressEvent(self, event):
        
        if event.key() == Qt.Key_Home:
            self.seek(0)
        
        elif event.key() == Qt.Key_End:
            self.seek(self.player.duration())
        
        elif event.key() == Qt.Key_C:
            self.addCut()
        
        elif event.key() == Qt.Key_Space:
            self.togglePlay()

        elif event.key() == Qt.Key_Delete:
            self.delCut()
        
        elif event.key() == Qt.Key_Right and event.modifiers() & Qt.ShiftModifier:
            self.jumpToCut(+1)
        
        elif event.key() == Qt.Key_Left and event.modifiers() & Qt.ShiftModifier:
            self.jumpToCut(-1)
        
        elif event.key() == Qt.Key_Left:
            self.seekBack()
        
        elif event.key() == Qt.Key_Right:
            self.seekForward()
            
        elif event.key() == Qt.Key_Up:
            if event.modifiers() & Qt.ShiftModifier:
                self.seekStep(+20000)
            else:
                self.seekStep(+10000)
            
        elif event.key() == Qt.Key_Down:
            if event.modifiers() & Qt.ShiftModifier:
                self.seekStep(-20000)
            else:
                self.seekStep(-10000)
           
            
            
    def jumpToCut(self, direction):
        # only one? go to it
        if self.cutList.count() <= 1:
            pos = self.cutList.itemData(0)
            if pos != None:
                self.seek(pos)
                return
        
        # current pos?
        pos = self.player.position()

        # find closest point in right direction
        if direction > 0:
            for cut in self.cutWidget.Cuts:
                if cut > pos+1:
                    self.seek(cut)
                    break
        
        elif direction < 0:
            for cut in reversed(self.cutWidget.Cuts):
                if cut <= pos-250:
                    self.seek(cut)
                    break
        
            

    def getSelectedPos(self):
        if self.cutList.count() == 0:
            return None
        
        index = self.cutList.currentIndex()
        return self.cutList.itemData(index)


    def getTimeStr(self, timeMillis):
        totalseconds = timeMillis / 1000.0        
        h = (totalseconds / 3600.0)
        m = (totalseconds / 60.0) % 60
        s = (totalseconds % 60)
        return '%02d:%02d:%05.2f' % (h, m, s)        
        
        
    def cutListSelectionChanged(self, index):
        if self.cutInProgress:
            self.setFocus()
            return
        
        pos = self.getSelectedPos()
        if pos != None:
            self.seek(pos)
        
        self.setFocus()
    
    
    def createButtons(self):
        self.btnSeekBack = QToolButton(self)
        self.btnSeekBack.clicked.connect(self.seekBack)
        self.btnSeekBack.setIcon(self.parent.getIcon("frame-back.png"))
        self.grid.addWidget(self.btnSeekBack, 2, 0)        
            
        self.btnPlayPause = QToolButton(self)
        self.btnPlayPause.clicked.connect(self.togglePlay)
        self.btnPlayPause.setIcon(self.parent.getIcon("play.png"))
        self.grid.addWidget(self.btnPlayPause, 2, 1)        
            
        self.btnSeekForward = QToolButton(self)
        self.btnSeekForward.clicked.connect(self.seekForward)
        self.btnSeekForward.setIcon(self.parent.getIcon("frame-forward.png"))
        self.grid.addWidget(self.btnSeekForward, 2, 2)        
        
        self.btnJump = QToolButton(self)
        self.btnJump.clicked.connect(self.jumpToSelectedCut)
        self.btnJump.setIcon(self.parent.getIcon("arrow_turn_left.png"))
        self.grid.addWidget(self.btnJump, 2, 4)
                    
        
        self.btnCut = QToolButton(self)
        self.btnCut.clicked.connect(self.addCut)
        self.btnCut.setIcon(self.parent.getIcon("cut.png"))
        self.grid.addWidget(self.btnCut, 2, 5)
        
        self.btnDelCut = QToolButton(self)
        self.btnDelCut.clicked.connect(self.delCut)
        self.btnDelCut.setIcon(self.parent.getIcon("delete.png"))
        self.grid.addWidget(self.btnDelCut, 2, 6)



    def jumpToSelectedCut(self):
        pos = self.getSelectedPos()
        
        if pos != None:
            self.seek(pos)
        

    
    def delCut(self):
        if self.cutInProgress:
            return
        else:
            self.cutInProgress = True

        try:
            selectedPos = self.getSelectedPos()
            if selectedPos != None:
                self.cutWidget.deleteCut(selectedPos)
                self.updateCutList(None)

        finally:
            self.cutInProgress = False
            
            
        
    def addCut(self):
        if self.cutInProgress:
            return
        else:
            self.cutInProgress = True
            
        try:
            pos = self.player.position()            
            self.cutWidget.addCut(pos)            
            self.updateCutList(pos)
        
        finally:
            self.cutInProgress = False



    def updateCutList(self, currentPos):
        
        self.cutList.clear()
        for cut in self.cutWidget.Cuts:
            str = "%s" % cut
            self.cutList.addItem(str, cut)
        
        if currentPos == None:
            return
        
        for i in range(len(self.cutWidget.Cuts)):
            if(self.cutList.itemData(i) == currentPos):
                self.cutList.setCurrentIndex(i)
                break
        
        
        
    def seekBack(self):
        self.seekStep(-240)



    def seekForward(self):
        self.seekStep(60)


    def seekStep(self, step):
        self.player.pause()
        currentPos = self.player.position()
        self.player.setPosition(currentPos + step)


    def togglePlay(self):
        state = self.player.state()
        
        if state == QMediaPlayer.PlayingState:
            self.player.pause()
        
        else:
            self.player.play()

    
    def createPlayer(self):
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.videoWidget)
        self.player.setVolume(5)

        self.player.durationChanged.connect(self.durationChanged)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.stateChanged.connect(self.stateChanged)
        self.player.videoAvailableChanged.connect(self.videoAvailableChanged)
        #self.player.mediaStatusChanged.connect(self.statusChanged)
        #self.player.bufferStatusChanged.connect(self.bufferingProgress)
        #self.player.error.connect(self.displayErrorMessage)
        
        self.probe = QVideoProbe()
        self.probe.videoFrameProbed.connect(self.processFrame)
        self.probe.setSource(self.player)


    def processFrame(self, frame):
        pass        
        
    
    def stateChanged(self, state):
        if state == QMediaPlayer.PlayingState:
            self.btnPlayPause.setIcon(self.parent.getIcon('pause.png'))
        else:
            self.btnPlayPause.setIcon(self.parent.getIcon('play.png'))
        
    
    
    def seek(self, milliseconds):
        if self.player.position() == milliseconds:
            return
        
        for i in range(self.cutList.count()):
            if self.cutList.itemData(i) == milliseconds:
                self.cutList.setCurrentIndex(i)
                break        
        
        self.player.setPosition(milliseconds)


    
    def durationChanged(self, duration):
        self.slider.setRange(0, duration)
        self.cutWidget.setDuration(duration)
        
    
    def positionChanged(self, progress):        
        if not self.slider.isSliderDown():
            self.slider.setValue(progress)
    
        self.cutWidget.setPosition(progress)
        self.timeLabel.setText(self.getTimeStr(progress))
    
    
    def videoAvailableChanged(self):
        print("availability: %s" % self.player.availability())
        
        
    def importCuts(self, cutMillis):
        if self.cutInProgress:
            return
        else:
            self.cutInProgress = True
            
        try:
            self.cutWidget.clear()
            self.cutList.clear()
            
            for cut in cutMillis:            
                self.cutWidget.addCut(cut)                
                self.updateCutList(cut)
        
        finally:
            self.cutInProgress = False
        
        
        
        