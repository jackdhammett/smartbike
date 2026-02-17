from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QLinearGradient, QColor, QPalette, QPainter
from App.StateManager import AppState
from App.chromium_controller import ChromiumController

from ui.screens.user_select import UserSelectScreen
from ui.screens.ride_setup import RideSetupScreen
from ui.screens.ride_active import RideActiveScreen
from ui.screens.ride_complete import RideCompleteScreen

from Services.BLE.cadence_stub import CadenceStub
from Services.metrics.ride_metrics import RideMetrics


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bike OS")
        self.chromium = ChromiumController()
        self.selected_user = None
        self.show_gradient_bg = True
        self.last_ride_stats = {}

        # Create stack widget
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("QStackedWidget { background: transparent; }")
        self.setCentralWidget(self.stack)

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.showFullScreen()
        
        # Screens
        self.user_select = UserSelectScreen(self)
        self.ride_setup = RideSetupScreen(self)
        self.ride_active = RideActiveScreen(self)
        self.ride_complete = RideCompleteScreen()

        self.stack.addWidget(self.user_select)
        self.stack.addWidget(self.ride_setup)
        self.stack.addWidget(self.ride_active)
        self.stack.addWidget(self.ride_complete)

        # Connect signals
        self.ride_complete.return_to_menu.connect(self.on_return_to_menu)
        self.cadence = CadenceStub()
        self.cadence.cadence_updated.connect(self.ride_active.update_cadence)

        self.set_state(AppState.USER_SELECT)

    def paintEvent(self, event):
        """Paint gradient background when show_gradient_bg is True."""
        if self.show_gradient_bg:
            painter = QPainter(self)
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor("#0a0e27"))  # Dark navy
            gradient.setColorAt(1, QColor("#000000"))  # Black
            painter.fillRect(self.rect(), gradient)
        super().paintEvent(event)

    def hide_background(self):
        """Hide the gradient background and make window transparent overlay."""
        self.show_gradient_bg = False
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.showFullScreen()
        self.update()

    def show_background(self):
        """Show the gradient background."""
        self.show_gradient_bg = True
        self.update()

    def set_state(self, state):
        if state == AppState.USER_SELECT:
            self.show_background()
            self.stack.setCurrentWidget(self.user_select)
            self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
            self.showFullScreen()

        elif state == AppState.RIDE_SETUP:
            self.show_background()
            self.stack.setCurrentWidget(self.ride_setup)
            self.ride_setup.update_user_label(self.selected_user)
            self.ride_setup.fade_in_ui(duration=1000, delay=200)

            self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
            self.showFullScreen()

        elif state == AppState.RIDE_ACTIVE:
            # Switch to overlay first
            self.stack.setCurrentWidget(self.ride_active)
            self.ride_active.fade_in_labels(duration=1000)

            # Force a repaint/update
            self.stack.repaint()

            # Then update window flags for transparency & top-most
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
            self.setAttribute(Qt.WA_TranslucentBackground, True)
            self.showFullScreen()

        elif state == AppState.RIDE_COMPLETE:
            self.show_background()
            self.stack.setCurrentWidget(self.ride_complete)
            self.ride_complete.set_ride_stats(self.last_ride_stats)
            self.ride_complete.fade_in_ui(duration=1000, delay=200)

            self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
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

    def on_return_to_menu(self):
        """Handle return to ride setup from completion screen"""
        self.ride_setup.show_leaderboard()
        self.set_state(AppState.RIDE_SETUP)
