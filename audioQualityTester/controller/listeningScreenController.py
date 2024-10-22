from pathlib import Path
import time
import json
import sys

from PySide6.QtCore import QObject, Slot, Signal, Property

from ..model.backend import BaseFactory
from ..model.audioProcessor import AudioProcessor, AudioPlotter
from ..model.audioPlayer import AudioPlayer
from ..model.logger import controllerLogger



class ListeningScreenController(QObject, BaseFactory):
    comboBoxElemsChanged = Signal()
    audioFileDuration = Signal(int)
    progressTextChanged = Signal()
    formattedResultChanged = Signal()
    errorMsg = Signal(str, name='errorMsg')


    def __init__(self, tempDir: dict, DEBUG: bool):
        super().__init__()

        self.DEBUG = DEBUG
        self._comboBoxElems = []
        self._formattedResult = []
        self.tempDir = tempDir
        self.playedExamples = []

        self._currentProgress = 0
        self.audioPlaying = 0
        self.startTime = None
        self.processor = None

        self.player = AudioPlayer()

        controllerLogger.debug(f'{self.__class__.__qualname__} initialized')
        return None

    @Property('QVariantList', notify=comboBoxElemsChanged)
    def comboBoxElems(self):
        return self._comboBoxElems
    

    def setComboBoxElems(self, newElems: list) ->  None:
        if newElems != self._comboBoxElems:
            self._comboBoxElems = newElems
            self.comboBoxElemsChanged.emit()
        
        return None


    def loadRandomAudio(self) -> tuple[dict, list]:

        randomAudioDict = self.loadJson(Path(self.tempDir['etc']) / 'randomizedAudioFiles.json')
                
        controllerLogger.debug('randomized audio file loaded')

        randomAudioDict = {int(key): value for key, value in randomAudioDict.items()}

        for value in randomAudioDict.values():
            value['path'] = Path(value['path'])
        
        comboBoxElems = sorted([value['name'] for value in randomAudioDict.values()])

        return randomAudioDict, comboBoxElems


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
    def setup(self) -> None:
        self.startTimeListeningScreen = time.time()

        self.settingDict = self.loadSettings()
        
        self.randomAudioDict, comboBoxElems = self.loadRandomAudio()

        self.audioFileDuration.emit(self.settingDict['metadata']['length'] - 5)

        self.setComboBoxElems(comboBoxElems)

        controllerLogger.debug('Listening Screen setup complete')
        return None
    
    # Expose getComboBoxElems as a Slot to make it callable from QML
    @Slot(result=list)
    def getComboBoxElems(self) -> list[str]:
        return self._comboBoxElems
    
    @Slot(result=bool)
    def isDebug(self) -> bool:
        return self.settingDict['debug']

    @Slot(int)
    def setCurrentProgress(self, progress) -> None:
        self._currentProgress = progress
        
        self.progressTextChanged.emit()
        return None

    @Property(str, notify=progressTextChanged)
    def progressText(self):
        minutes, seconds = divmod(self._currentProgress, 60)
        return f'{minutes:02d}:{seconds:02d}'

    @Slot(str, int)
    def play(self, buttonName:str, startTime: int = 0) -> None:
        key = int(buttonName.split('_')[1]) - 1


        if self.settingDict['statusDict']['audioOnce']:

            if key in self.playedExamples:
                errorMsg = 'Error: Play audio only once was selected'
                self.errorMsg.emit(errorMsg)
                self.stop()
                return None
            else:

                self.playedExamples.append(key)

        audioFile = self.randomAudioDict[key]['path']
        controllerLogger.info(f"start file {audioFile}")

        self._managePlayDuration()
        self.player.playFile(audioFile, startTime)
        self.player.managePlaying(key)

        return None
    
    @Slot()
    def stop(self) -> None:
        self.player.stopFile()

        self._managePlayDuration()
        return None


    def _managePlayDuration(self) -> None:
        key, duration = self.player.manageStopping()
        
        if key is not None:
            self.randomAudioDict[key]['listeningDuration'] += duration
        return None

    @Slot("QVariantMap")
    def submitButtonPressed(self, comboBoxChoices:dict[str:str]) -> None:

        controllerLogger.debug('Submit button pressed')
        controllerLogger.info(f'comboBox choices: {comboBoxChoices}')

        self.stop()
        duration = int(round(self.startTimeListeningScreen - time.time()))

        self.processor = AudioProcessor(tempDir=self.tempDir,
                                       randomAudioDict=self.randomAudioDict, 
                                       statusDict=self.settingDict['statusDict'],
                                       compressionDict=self.settingDict['compressionDict']
                                        )
        
        result = self.processor.computeResult(comboBoxChoices, duration)
        
        controllerLogger.warning(self.settingDict['statusDict'])
        plotter = AudioPlotter(self.tempDir['images'], self.settingDict['statusDict']['debug'])
        result = plotter.plotAllResults(result)

        self._formattedResult = self.processor.formatResult(result)

        return None

    @Slot(result='QVariant')
    def getFormatResult(self) -> list[dict[str, str]]:
        return self._formattedResult

