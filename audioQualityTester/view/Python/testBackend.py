from PySide6.QtCore import QObject, Slot

class MyBackend(QObject):
    def __init__(self):
        super().__init__()

    # Define a slot that can be called from QML
    @Slot()
    def start_button_pressed(self):
        print("Start button was pressed!")