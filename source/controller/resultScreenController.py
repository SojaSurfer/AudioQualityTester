from pathlib import Path
import json
import sys

from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWidgets import QFileDialog

from ..model.backend import BaseFactory
from ..model.resultHandler import ResultHandler
from ..model.logger import controllerLogger



class ResultScreenController(QObject, BaseFactory):
    resultChanged = Signal(dict)

    def __init__(self, tempDir:dict, **kwargs):
        super().__init__()

        self.tempDir = tempDir

        self.resultDict = kwargs.get('result', {})
        
        self.resultHandler = ResultHandler()

        self.resultChanged.emit(self.resultDict)
        
        controllerLogger.debug(f'{self.__class__.__qualname__} initialized')
        return None
    
    @Slot()
    def setup(self):
        self.settingsDict = self.loadSettings()
        return None


    def loadSettings(self) -> dict:
        try:
            with open(Path(self.tempDir['etc']) / 'settings.json', 'r') as file:
                settings = json.load(file)

        except FileNotFoundError:
            # temporary directory was not created fall back to debug data in test directory
            self.tempDir = self.getTempDirDEBUG()
            with open(self.tempDir['etc'] / 'settings.json', 'r') as file:
                settings = json.load(file)
            
            assert settings['statusDict']['debug'], "debug temp directory was loaded even though it was not checked!"
        
        return settings

    @Slot()
    def saveDataButtonPressed(self):
        controllerLogger.debug(f'SaveData button pressed')

        # Open the dialog to select a file
        fileDialog = QFileDialog()
        outputPath = fileDialog.getExistingDirectory(None, "Select Directory", "")
        
        if outputPath:
            self.resultHandler.zipDirectory(self.tempDir['root'], outputPath)


        return None
    
    @Slot()
    def exitButtonPressed(self):
        controllerLogger.debug(f'Exit button pressed')

        # clean up
        return None
    
    @Slot()
    def restartButtonPressed(self):
        controllerLogger.debug(f'Restart button pressed')

    @Slot()
    def backButtonPressed(self):
        controllerLogger.debug(f'Back button pressed')
        return None

