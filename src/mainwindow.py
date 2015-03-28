#!/usr/bin/env python

import os
import re
import threading
import subprocess

from mainwidget import MainWidget

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from localization import LC


### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


class MainWindow(QMainWindow):    
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        # Settings
        self.setWindowTitle("Poor Man's Video Cutter")
        self.resize(800, 560)
        self.lastFolder = os.path.expanduser("~")
        self.currentFile = ''
        
        # build content
        self.Content = MainWidget(self)
        self.Content.setEnabled(False)
        self.setCentralWidget(self.Content)
        
        # menu & toolbar
        self.createMenu()
        self.createToolbar()
        
        #self.statusBar().addWidget(QLabel("ready"))
        
        #action = menu.addAction('Change File Path')
        #action.triggered.connect(self.changeFilePath)
        
        #print(action.icon)
        
        
        
    def createMenu(self):
        menu = self.menuBar().addMenu(LC('menu.file.title'))
        
        self.openAction = self.createMenuItem(menu, LC('menu.file.open'), 'open.png', 'CTRL+O', self.open)
        self.saveAction = self.createMenuItem(menu, LC('menu.file.save'), 'disk.png', 'CTRL+S', self.save)
        self.saveAction.setEnabled(False)
        menu.addSeparator()

        self.exportEdlAction = self.createMenuItem(menu, LC('menu.file.exportlist'), 'table_save.png', None, self.exportList)
        self.exportEdlAction.setEnabled(False)
        menu.addSeparator()
        
        self.createMenuItem(menu, LC('menu.file.close'), 'exit.png', 'CTRL+Q', self.close)
        
        
    def createToolbar(self):
        toolbar = self.addToolBar('toolbar')
                
        toolbar.addAction(self.openAction)
        toolbar.addAction(self.saveAction)
        toolbar.addSeparator()
        
        toolbar.addAction(self.exportEdlAction)
    
    
    
    def getIcon(self, icon):
        if icon == None:
            return None
        
        selfPath = os.path.dirname(__file__)        
        iconPath = os.path.join(selfPath, 'icons', icon)
        return QIcon(iconPath)                     


    def createMenuItem(self, parent, title, icon, shortcut, callback):
        action = parent.addAction(title)
        
        icon = self.getIcon(icon)
        if icon != None:
            action.setIcon(icon)
        
        if shortcut != None:
            action.setShortcut(shortcut)
        
        if callback != None:
            action.triggered.connect(callback)
        
        return action


    def saveLastFolder(self, filename):
        self.lastFolder = os.path.dirname(filename)



    def save(self):
        # get keep parts
        timecodes = []
        parts = self.generateSections(True)
        for part in parts:
            timeA = self.Content.getTimeStr(part[0])
            timeB = self.Content.getTimeStr(part[1])
            timecodes.append("%s-%s" % (timeA, timeB))
        
        cmdArg = ",+".join(timecodes)
        cmdArg = "--split parts:" + cmdArg

        filter = 'Matroska MKV (*.mkv)'
        suggest = self.changeFileExtension(self.currentFile, ".cut.mkv")
        print(suggest)        
        filename, filter = QFileDialog.getSaveFileName(directory = suggest, filter=filter)        
        if filename == '':
            return

        self.saveLastFolder(filename)
        cmd = 'mkvmerge -o "%s" "%s" %s' % (filename, self.currentFile, cmdArg)
        self.executeCommand(cmd, LC("text.wait"), None)



    def executeCommand(self, command, message, btn):
        def doCmd():
            result = subprocess.call(command, shell=True)
            print("command '%s' has exit with %s" % (command, result))                        
        
        self.executeWithDialog(doCmd, message, btn)
        


    def executeWithDialog(self, callback, message, btn):
        progress = QProgressDialog(message, btn, 0, 0, self)
        progress.show()        

        def doCallback():
            try:
                callback()
            finally:
                progress.close()
        
        t = threading.Thread(target=doCallback)
        t.start()

            
            
    def exportList(self):
        #option for directory: directory='/mnt/', 
        filter = 'EDL Cutlist (*.edl)'
        suggest = self.getEDLFile(self.currentFile)        
        filename, filter = QFileDialog.getSaveFileName(directory = suggest, filter=filter)        
        if filename == '':
            return
        
        self.saveLastFolder(filename)        
        with open(filename, 'w') as f:
            edlSections = self.generateSections(False)
            for sec in edlSections:
                str = "%04.2f\t%04.2f\t0\n" % (sec[0]/1000.0, sec[1]/1000.0)
                f.write(str)
        

    
    def generateSections(self, keepSections = True):
        result = []
        times = []
        cuts = self.Content.cutWidget.Cuts + [self.Content.player.duration()]
        
        if not keepSections:
            times.append(0)
        
        for cut in cuts:
            times.append(cut)
            if len(times) == 2:            
                result.append((times[0], times[1]))
                times.clear()
        
        return result
        
        
            
    def open(self):
        videoFileFilters = (
            "Matroska MKV (*.mkv)",
            "AVI-Container (*.avi)" 
        )
        
        vidfilter = ";;".join(videoFileFilters)
        filename, filter = QFileDialog.getOpenFileName(directory = self.lastFolder, filter=vidfilter)
        if filename == '':
            return
        
        self.saveLastFolder(filename)
        self.loadFile(filename)
    
    
    
    def loadFile(self, filename):
        self.currentFile = filename        
        self.Content.Open(filename)
        
        # some edl? import
        edlFile = self.getEDLFile(filename)
        print(edlFile)
        if os.path.isfile(edlFile):
            self.importEDL(edlFile)
        
        self.saveAction.setEnabled(True)
        self.exportEdlAction.setEnabled(True)
        self.Content.setEnabled(True)
            
            

    def importEDL(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        pattern = r'^([0-9\.]+)\s+([0-9\.]+)\s+[0123]$'
        cuts = []
        for line in lines:
            m = re.search(pattern, line)
            timeBegin = m.group(1)
            timeEnd = m.group(2)
            cuts.append(float(timeBegin) * 1000)
            cuts.append(float(timeEnd) * 1000)
            
        self.Content.importCuts(cuts[1:-1])


    def getEDLFile(self, filename):
        return self.changeFileExtension(filename, ".edl")
            
    
    
    def changeFileExtension(self, filename, newExt):
        file, ext = os.path.splitext(filename)
        return file + newExt
    
    
    
    def close(self):
        app = QApplication.instance()
        app.closeAllWindows()        

