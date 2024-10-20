from pathlib import Path
import sys

from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWidgets import QFileDialog

from ..model.backend import StartSettingInspector, BaseFactory
from ..model.audioProcessor import AudioProcessor
from ..model.logger import controllerLogger



class StartScreenController(QObject, BaseFactory):
    """The class is the controller of the Qt start screen page.
    
    Arguments:
        tempDir (dict): A dict for the paths.
    
    """
    
    # Define a signal to send the selected file path to QML
    filePathSelected = Signal(str)
    originalAudioFormat = Signal(str)
    correctSettings = Signal(bool)
    errorMsg = Signal(str, name='errorMsg')

    def __init__(self, tempDir:dict, DEBUG: bool = False):
        super().__init__()

        self.tempDir = tempDir
        self.DEBUG = DEBUG

        self.settingInspector = None
        self.inputAudioFormat = ("MP3_cbr320", 'MP3 [320 kbps]') # None

        controllerLogger.debug(f'{self.__class__.__qualname__} initialized')
        return None

    @Slot(result=bool)
    def getDebugState(self) -> bool:
        return self.DEBUG

    @Slot()
    def fileLoadButtonPressed(self):
        controllerLogger.debug(f'file load button pressed')
        # Create a QFileDialog instance
        fileDialog = QFileDialog()

        # Open the dialog to select a file
        audioFilter = ' '.join([f'*.{audioFormat.lower()}' for audioFormat in self.SUPPORTED_AUDIOFILES])
        fileFilter = f"Audio ({audioFilter});;All Files (*)"

        filepath, _ = fileDialog.getOpenFileName(None, "Select File", "", fileFilter)
        
        if filepath:
            controllerLogger.debug(f"fileLoadButton file changed: {filepath}")
            # Emit the selected file path
            self.filePathSelected.emit(filepath)

            settingInspector = StartSettingInspector()
            settingInspector.loadMetadata(filepath)
            self.inputAudioFormat = settingInspector.returnAudioFormat(format=2)

        else:
            controllerLogger.debug("fileLoadButton no file selected")
            self.filePathSelected.emit("")
        
        return None


    @Slot("QVariantMap", "QVariantMap")
    def startButtonPressed(self, statusDict:dict, compressionDict:list[dict]):

        controllerLogger.info("Start button was pressed")

        # for key, value in statusDict.items():
        #     controllerLogger.info(key, ':', value, type(value))
        
        # for key, value in compressionDict.items():
        #     controllerLogger.info(key, value)
        

        self.settingInspector = StartSettingInspector()
        if self.settingInspector.validateUserInput(statusDict=statusDict, compressionDict=compressionDict):

            audioFormat = self.settingInspector.returnAudioFormat()

            processor = AudioProcessor(tempDir=self.tempDir,
                                       statusDict=statusDict, 
                                       compressionDict=compressionDict,
                                       audioFormat=audioFormat,
                                       metadata=self.settingInspector.metadata,
                                       inputAudioFormat=self.inputAudioFormat[0])
            
            processor.setup()

            self.correctSettings.emit(True)

        self.errorMsg.emit(self.settingInspector.errorMsg)

        return None
    
    @Slot(result='QVariant')
    def getCompressionOptions(self) -> list[dict]:
        
        if self.DEBUG:
            compressionOptionsPath = Path(__file__).parent.parent / 'resources' / 'CompressionOptionsDebug.json'
        else:
            compressionOptionsPath = Path(__file__).parent.parent / 'resources' / 'CompressionOptions.json'
        
        defaultOptions = self.loadJson(compressionOptionsPath)


        if self.inputAudioFormat is not None:

            if all([self.inputAudioFormat[0] != audioFormat["identifier"] for audioFormat in defaultOptions]):
                defaultOptions.insert(0, {"identifier": self.inputAudioFormat[0], "text": self.inputAudioFormat[1], "selected": False})

                controllerLogger.info(f'Added orig. audio file format to default options: {self.inputAudioFormat[0]}')
            else:
                controllerLogger.info(f'Loaded orig. audio file format in default options: {self.inputAudioFormat[0]}')

        
        return defaultOptions

