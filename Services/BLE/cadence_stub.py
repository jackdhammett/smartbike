from PyQt5.QtCore import QObject, QTimer, pyqtSignal
import random

class CadenceStub(QObject):
    cadence_updated = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.generate)
        self.timer.start(1000)

    def generate(self):
        rpm = random.randint(70, 100)
        self.cadence_updated.emit(rpm)
