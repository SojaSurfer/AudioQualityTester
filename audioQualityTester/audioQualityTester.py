# Copyright (C) 2024 Julian Wagner
# This file is part of the AudioQualityTester project.
#
# AudioQualityTester is under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# AudioQualityTester is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with AudioQualityTester. If not, see <http://www.gnu.org/licenses/>.


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
from .model.errorHandler import verifyExternalDependencies
from .model.logger import mainLogger, installCustomMessageHandlerQT


__license__ = 'GNU-GPL-3.0-only'
__all__ = ['main']




@tempDirWrapper
def main(tempDir:dict, DEBUG: bool = False) -> None:
    mainLogger.info('Starting main()')

    verifyExternalDependencies()
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
    lsController = ListeningScreenController(tempDir, DEBUG)
    rsController = ResultScreenController(tempDir, DEBUG=DEBUG)


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

