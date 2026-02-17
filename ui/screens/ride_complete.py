from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor


class RideCompleteScreen(QWidget):
    return_to_menu = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1a1a2e;")
        
        # Main layout - center everything
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addStretch()

        # Dashboard container
        dashboard = QFrame()
        dashboard.setStyleSheet("background-color: rgba(26, 26, 46, 0.8); border-radius: 16px; border: none;")
        dashboard.setFixedWidth(600)
        dashboard.setFixedHeight(500)
        
        dashboard_layout = QVBoxLayout()
        dashboard_layout.setContentsMargins(40, 40, 40, 40)
        dashboard_layout.setSpacing(24)

        # Title
        title = QLabel("Ride Complete!")
        title_font = QFont("Segoe UI", 40, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00D4FF;")
        dashboard_layout.addWidget(title)

        # Stats grid (2x2)
        stats_grid = QVBoxLayout()
        stats_grid.setSpacing(20)

        # Row 1: Cadence and Speed
        row1 = QHBoxLayout()
        row1.setSpacing(30)
        
        cadence_col = QVBoxLayout()
        cadence_col.setSpacing(4)
        cadence_label = QLabel("Average Cadence")
        cadence_label.setFont(QFont("Segoe UI", 12))
        cadence_label.setStyleSheet("color: #AAAAAA;")
        cadence_label.setAlignment(Qt.AlignCenter)
        self.cadence_display = QLabel("0 RPM")
        self.cadence_display.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.cadence_display.setStyleSheet("color: #00D4FF;")
        self.cadence_display.setAlignment(Qt.AlignCenter)
        cadence_col.addWidget(cadence_label)
        cadence_col.addWidget(self.cadence_display)
        
        speed_col = QVBoxLayout()
        speed_col.setSpacing(4)
        speed_label = QLabel("Average Speed")
        speed_label.setFont(QFont("Segoe UI", 12))
        speed_label.setStyleSheet("color: #AAAAAA;")
        speed_label.setAlignment(Qt.AlignCenter)
        self.speed_display = QLabel("0 MPH")
        self.speed_display.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.speed_display.setStyleSheet("color: #00D4FF;")
        self.speed_display.setAlignment(Qt.AlignCenter)
        speed_col.addWidget(speed_label)
        speed_col.addWidget(self.speed_display)
        
        row1.addLayout(cadence_col)
        row1.addLayout(speed_col)
        stats_grid.addLayout(row1)

        # Row 2: Calories and Time
        row2 = QHBoxLayout()
        row2.setSpacing(30)
        
        calories_col = QVBoxLayout()
        calories_col.setSpacing(4)
        calories_label = QLabel("Total Calories")
        calories_label.setFont(QFont("Segoe UI", 12))
        calories_label.setStyleSheet("color: #AAAAAA;")
        calories_label.setAlignment(Qt.AlignCenter)
        self.calories_display = QLabel("0")
        self.calories_display.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.calories_display.setStyleSheet("color: #00D4FF;")
        self.calories_display.setAlignment(Qt.AlignCenter)
        calories_col.addWidget(calories_label)
        calories_col.addWidget(self.calories_display)
        
        time_col = QVBoxLayout()
        time_col.setSpacing(4)
        time_label = QLabel("Total Time")
        time_label.setFont(QFont("Segoe UI", 12))
        time_label.setStyleSheet("color: #AAAAAA;")
        time_label.setAlignment(Qt.AlignCenter)
        self.time_display = QLabel("00:00")
        self.time_display.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.time_display.setStyleSheet("color: #00D4FF;")
        self.time_display.setAlignment(Qt.AlignCenter)
        time_col.addWidget(time_label)
        time_col.addWidget(self.time_display)
        
        row2.addLayout(calories_col)
        row2.addLayout(time_col)
        stats_grid.addLayout(row2)

        dashboard_layout.addLayout(stats_grid)
        dashboard.setLayout(dashboard_layout)

        # Create centered container for dashboard
        dashboard_container = QVBoxLayout()
        dashboard_container.addWidget(dashboard, alignment=Qt.AlignCenter)
        main_layout.addLayout(dashboard_container)

        # Return to Menu button - oval shape, below dashboard
        button_container = QVBoxLayout()
        button_container.setContentsMargins(0, 40, 0, 0)
        return_btn = QPushButton("Return to Menu")
        return_btn.setFont(QFont("Segoe UI", 16, QFont.Bold))
        return_btn.setFixedWidth(220)
        return_btn.setFixedHeight(70)
        return_btn.setStyleSheet("""
            QPushButton {
                background-color: #00D4FF;
                color: #1a1a2e;
                border: none;
                border-radius: 35px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00B8D4;
            }
            QPushButton:pressed {
                background-color: #0099AA;
            }
        """)
        return_btn.clicked.connect(self.on_return_clicked)
        button_container.addWidget(return_btn, alignment=Qt.AlignCenter)
        main_layout.addLayout(button_container)

        main_layout.addStretch()
        self.setLayout(main_layout)

    def set_ride_stats(self, stats):
        """Update display with ride statistics"""
        self.cadence_display.setText(f"{int(stats.get('cadence', 0))} RPM")
        self.speed_display.setText(f"{stats.get('speed', 0):.1f} MPH")
        self.calories_display.setText(f"{int(stats.get('calories', 0))}")
        self.time_display.setText(stats.get('time', '00:00'))

    def on_return_clicked(self):
        self.return_to_menu.emit()

    def fade_in_ui(self, duration=1000, delay=0):
        """Fade in the ride complete screen"""
        from PyQt5.QtCore import QPropertyAnimation, QTimer
        
        def start_animation():
            anim = QPropertyAnimation(self, b"windowOpacity")
            anim.setDuration(duration)
            anim.setStartValue(0.0)
            anim.setEndValue(1.0)
            anim.start()
            self._anim = anim
        
        if delay > 0:
            QTimer.singleShot(delay, start_animation)
        else:
            start_animation()
