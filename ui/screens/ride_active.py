from ui.components.stat_tile import StatTile
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPropertyAnimation

class RideActiveScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setAttribute(Qt.WA_TranslucentBackground)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Stats box
        self.stats_box = QFrame(self)
        self.stats_box.setStyleSheet("background-color: rgba(0,0,0,150); border-radius: 15px;")
        self.stats_box.setFixedSize(320, 220)

        stats_layout = QVBoxLayout()
        stats_layout.setContentsMargins(20, 20, 20, 20)
        stats_layout.setSpacing(15)

        # Labels
        self.cadence_label = QLabel("Cadence: 0 RPM")
        self.speed_label = QLabel("Speed: 0 km/h")
        self.calories_label = QLabel("Calories: 0 kcal")
        self.labels = [self.cadence_label, self.speed_label, self.calories_label]

        for lbl in self.labels:
            lbl.setStyleSheet("color: white; font-size: 26px; background: transparent;")
            lbl.setAlignment(Qt.AlignCenter)

            # Add subtle glow/shadow
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(8)
            shadow.setColor(Qt.white)  # or QColor(255,255,255,200) for semi-transparent
            shadow.setOffset(0)
            lbl.setGraphicsEffect(shadow)

            # Start invisible for fade-in
            lbl.setWindowOpacity(0.0)

            stats_layout.addWidget(lbl)

        self.stats_box.setLayout(stats_layout)
        main_layout.addWidget(self.stats_box, alignment=Qt.AlignTop | Qt.AlignLeft)
        main_layout.addStretch()
        self.setLayout(main_layout)

    # --------------------------
    # Fade-in animation for all labels
    # --------------------------
    def fade_in_labels(self, duration=1000):
        for lbl in self.labels:
            anim = QPropertyAnimation(self.stats_box, b"windowOpacity")
            anim.setDuration(duration)
            anim.setStartValue(0.0)
            anim.setEndValue(1.0)
            anim.start()
            # Keep reference to prevent garbage collection
            self.stats_box._anim = anim

    def update_cadence(self, rpm):
        self.cadence_label.setText(f"Cadence: {rpm} RPM")
        self.speed_label.setText(f"Speed: {round(rpm*0.3,1)} km/h")
        self.calories_label.setText(f"Calories: {round(rpm*0.05,1)} kcal")
