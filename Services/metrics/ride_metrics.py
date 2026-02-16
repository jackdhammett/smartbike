from PyQt5.QtCore import QObject, pyqtSignal

class RideMetrics(QObject):
    metrics_updated = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.cadence = 0
        self.speed = 0
        self.calories = 0

    def update_cadence(self, rpm):
        self.cadence = rpm
        self.speed = round(rpm * 0.3, 1)
        self.calories += round(rpm * 0.05, 1)

        self.metrics_updated.emit({
            "cadence": self.cadence,
            "speed": self.speed,
            "calories": self.calories
        })
