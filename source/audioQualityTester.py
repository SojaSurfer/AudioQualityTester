import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

# from rich import traceback, print
# traceback.install()

from .controller.startScreenController import StartScreenController
from .controller.listeningScreenController import ListeningScreenController
from .controller.resultScreenController import ResultScreenController
from .model.backend import tempDirWrapper
from .model.logger import mainLogger, installCustomMessageHandlerQT


__version__ = '0.1'
__license__ = 'GNU-GPL-3.0-only'
__all__ = ['main', 'DEBUG']


global DEBUG
DEBUG = False



@tempDirWrapper
def main(tempDir:dict) -> None:
    mainLogger.info('Starting main()')

    assert tempDir['images'].exists(), f'not a file: {tempDir["images"]}'
    sourceDir = Path(__file__).absolute().expanduser().parent
    appPath = sourceDir / 'view' / 'ProjectContent' / 'App.qml'
    importPaths = [".", 'view/Project']

    installCustomMessageHandlerQT()
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    engine.addImportPath(sourceDir)
    for path in importPaths:
        engine.addImportPath(sourceDir / path)

    # Add this right after setting import paths
    for path in engine.importPathList():
        mainLogger.info(f'QML Import Path: {path}')
    

    ssController = StartScreenController(tempDir, DEBUG)
    lsController = ListeningScreenController(tempDir)
    rsController = ResultScreenController(tempDir)


    engine.rootContext().setContextProperty("startScreenController", ssController)
    engine.rootContext().setContextProperty("listeningScreenController", lsController)
    engine.rootContext().setContextProperty("resultScreenController", rsController)
    mainLogger.debug('Connected the controller to the UI engine')

    # engine.warnings.connect(log_qml_warning)
    engine.load(appPath)
    mainLogger.debug(f'Loaded {appPath.name}')

    if not engine.rootObjects():
        mainLogger.error('engine is not root object')
        sys.exit(-1)


    exitCode = app.exec()
    mainLogger.info(f'UI terminated with exitcode {exitCode}')
    sys.exit(exitCode)

    return None



if __name__ == "__main__":

    mainLogger.debug('Module import complete')
    main()

