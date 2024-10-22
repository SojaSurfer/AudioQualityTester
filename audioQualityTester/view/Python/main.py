
import os
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from testBackend import MyBackend  # Import the backend class

from autogen.settings import url, import_paths

from rich import traceback, print
traceback.install()



if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    app_dir = Path(__file__).parent.parent

    engine.addImportPath(os.fspath(app_dir))
    for path in import_paths:
        engine.addImportPath(os.fspath(app_dir / path))

    backend = MyBackend()
    engine.rootContext().setContextProperty("backend", backend)

    print(os.fspath(app_dir/url))
    engine.load(os.fspath(app_dir/url))
    print(2)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())

