from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from App.StateManager import AppState
from App.chromium_controller import ChromiumController

from ui.screens.user_select import UserSelectScreen
from ui.screens.ride_setup import RideSetupScreen
from ui.screens.ride_active import RideActiveScreen

from Services.BLE.cadence_stub import CadenceStub
from Services.metrics.ride_metrics import RideMetrics


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bike OS")
        self.setStyleSheet("color: white;")

        self.chromium = ChromiumController()
        self.selected_user = None
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;") 
        self.showFullScreen()
        
        # Screens
        self.user_select = UserSelectScreen(self)
        self.ride_setup = RideSetupScreen(self)
        self.ride_active = RideActiveScreen(self)

        self.stack.addWidget(self.user_select)
        self.stack.addWidget(self.ride_setup)
        self.stack.addWidget(self.ride_active)

        # Services (stub)
        self.cadence = CadenceStub()
        self.cadence.cadence_updated.connect(self.ride_active.update_cadence)

        self.set_state(AppState.USER_SELECT)

    def set_state(self, state):
        if state == AppState.USER_SELECT:
            self.stack.setCurrentWidget(self.user_select)
            # Normal fullscreen window
            self.setWindowFlags(Qt.Window)
            self.showFullScreen()

        elif state == AppState.RIDE_SETUP:
            self.stack.setCurrentWidget(self.ride_setup)
            self.ride_setup.update_user_label(self.selected_user)
            self.ride_setup.fade_in_ui(duration=1000, delay=200)

            self.setWindowFlags(Qt.Window)
            self.setAttribute(Qt.WA_TranslucentBackground, False)
            self.showFullScreen()

        elif state == "RIDE_ACTIVE":
            # Create overlay if it doesn’t exist
            if not hasattr(self, "ride_active") or self.ride_active is None:
                self.ride_active = RideActiveScreen(self)
                self.stack.addWidget(self.ride_active)

            # Switch to overlay first
            self.stack.setCurrentWidget(self.ride_active)
            self.ride_active.fade_in_labels(duration=1000)

            # Force a repaint/update
            self.stack.repaint()

            # Then update window flags for transparency & top-most
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
            self.setAttribute(Qt.WA_TranslucentBackground, True)
            self.showFullScreen()

    def activate_overlay(self):
        """Make window transparent overlay on top of media."""
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()
