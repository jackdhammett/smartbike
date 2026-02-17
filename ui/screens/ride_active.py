from ui.components.stat_tile import StatTile
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QGraphicsDropShadowEffect, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer, QTime
from PyQt5.QtGui import QColor
from App.StateManager import AppState

class RideActiveScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setAttribute(Qt.WA_TranslucentBackground)

        # Ride tracking
        self.cadence_readings = []
        self.speed_readings = []
        self.total_calories = 0
        self.ride_start_time = QTime()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Stats row - thin horizontal bar at top
        self.stats_row = QFrame(self)
        self.stats_row.setStyleSheet("background-color: rgba(10, 14, 39, 200); border: none;")
        self.stats_row.setFixedHeight(60)

        stats_row_layout = QHBoxLayout()
        stats_row_layout.setContentsMargins(30, 8, 30, 8)
        stats_row_layout.setSpacing(60)

        # Cadence
        self.cadence_label = QLabel("Cadence: 0 RPM")
        self.cadence_label.setStyleSheet("color: #00d9ff; font-size: 16px; background: transparent; font-weight: 500;")
        self.cadence_label.setAlignment(Qt.AlignCenter)
        stats_row_layout.addWidget(self.cadence_label)

        # Speed
        self.speed_label = QLabel("Speed: 0 mph")
        self.speed_label.setStyleSheet("color: #00d9ff; font-size: 16px; background: transparent; font-weight: 500;")
        self.speed_label.setAlignment(Qt.AlignCenter)
        stats_row_layout.addWidget(self.speed_label)

        # Calories
        self.calories_label = QLabel("Calories: 0 kcal")
        self.calories_label.setStyleSheet("color: #00d9ff; font-size: 16px; background: transparent; font-weight: 500;")
        self.calories_label.setAlignment(Qt.AlignCenter)
        stats_row_layout.addWidget(self.calories_label)

        # Time
        self.time_label = QLabel("Time: 00:00")
        self.time_label.setStyleSheet("color: #00d9ff; font-size: 16px; background: transparent; font-weight: 500;")
        self.time_label.setAlignment(Qt.AlignCenter)
        stats_row_layout.addWidget(self.time_label)

        # End Ride button
        self.end_ride_btn = QPushButton("End Ride")
        self.end_ride_btn.clicked.connect(self.end_ride)
        self.end_ride_btn.setStyleSheet("""
            QPushButton {
                color: #ffffff;
                font-size: 12px;
                font-weight: 600;
                background-color: #d91e1e;
                border: 1px solid #a01818;
                border-radius: 4px;
                padding: 4px 12px;
            }
            QPushButton:hover {
                background-color: #e52e2e;
                border: 1px solid #ff4444;
            }
            QPushButton:pressed {
                background-color: #c01010;
            }
        """)
        self.end_ride_btn.setCursor(Qt.PointingHandCursor)
        self.end_ride_btn.setFixedWidth(80)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(6)
        shadow.setColor(QColor(217, 30, 30, 40))
        shadow.setOffset(0, 1)
        self.end_ride_btn.setGraphicsEffect(shadow)
        
        stats_row_layout.addStretch()
        stats_row_layout.addWidget(self.end_ride_btn)

        self.stats_row.setLayout(stats_row_layout)
        main_layout.addWidget(self.stats_row, alignment=Qt.AlignTop)
        main_layout.addStretch()
        
        self.setLayout(main_layout)

    def fade_in_labels(self, duration=1000):
        """Fade in stats row"""
        anim = QPropertyAnimation(self.stats_row, b"windowOpacity")
        anim.setDuration(duration)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.start()
        self.stats_row._anim = anim
        
        # Start ride timer
        self.ride_start_time = QTime(0, 0, 0)
        self.timer.start(1000)  # Update every second

    def update_time(self):
        """Update elapsed time"""
        self.ride_start_time = self.ride_start_time.addSecs(1)
        time_str = self.ride_start_time.toString("mm:ss")
        self.time_label.setText(f"Time: {time_str}")

    def update_cadence(self, rpm):
        """Update cadence and derived metrics"""
        # Track readings
        self.cadence_readings.append(rpm)
        
        # Calculate speed from cadence (rpm * 0.3 km/h → convert to mph)
        speed_kmh = round(rpm * 0.3, 1)
        speed_mph = round(speed_kmh * 0.621371, 1)  # Convert km/h to mph
        self.speed_readings.append(speed_mph)
        
        # Calculate calories (rpm * 0.05)
        calories_delta = round(rpm * 0.05, 2)
        self.total_calories += calories_delta
        
        # Update display
        self.cadence_label.setText(f"Cadence: {rpm} RPM")
        self.speed_label.setText(f"Speed: {speed_mph} mph")
        self.calories_label.setText(f"Calories: {int(self.total_calories)} kcal")
    
    def end_ride(self):
        """End the ride and transition to ride complete screen"""
        self.timer.stop()
        
        # Calculate averages
        avg_cadence = round(sum(self.cadence_readings) / len(self.cadence_readings)) if self.cadence_readings else 0
        avg_speed = round(sum(self.speed_readings) / len(self.speed_readings), 1) if self.speed_readings else 0
        total_calories = int(self.total_calories)
        elapsed_time = self.time_label.text().replace("Time: ", "")
        
        # Store ride data
        self.main_window.last_ride_stats = {
            'cadence': avg_cadence,
            'speed': avg_speed,
            'calories': total_calories,
            'time': elapsed_time
        }
        self.main_window.set_state(AppState.RIDE_COMPLETE)
