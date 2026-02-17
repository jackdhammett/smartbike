from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QSequentialAnimationGroup, QPropertyAnimation
from App.StateManager import AppState
from App.config import DEFAULT_MEDIA_URL

class RideSetupScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setSpacing(40)
        layout.setContentsMargins(100, 100, 100, 100)
        layout.setAlignment(Qt.AlignCenter)

        # Label above user selection
        self.user_label = QLabel("Welcome, ")
        self.user_label.setAlignment(Qt.AlignCenter)
        self.user_label.setStyleSheet("color: white; font-size: 36px; background: transparent;")
        layout.addWidget(self.user_label)
        
        # Horizontal button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(50)
        button_layout.setAlignment(Qt.AlignCenter)

        # Start Ride button
        self.start_ride_btn = QPushButton("Start Ride")
        self.start_ride_btn.clicked.connect(lambda: main_window.set_state("RIDE_ACTIVE"))
        self.style_tile_button(self.start_ride_btn)
        button_layout.addWidget(self.start_ride_btn)

        # Launch Media button
        self.launch_media_btn = QPushButton("Launch Media")
        self.launch_media_btn.clicked.connect(self.launch_media)
        self.style_tile_button(self.launch_media_btn)
        button_layout.addWidget(self.launch_media_btn)
        # Store buttons for fade-in animation
        self.buttons = [self.start_ride_btn, self.launch_media_btn]
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.user_label.setWindowOpacity(0.0)
        for btn in self.buttons:
            btn.setWindowOpacity(0.0)

    def style_tile_button(self, button: QPushButton):
        button.setFixedSize(250, 100)  # width x height
        button.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 28px;
                background-color: rgba(255,255,255,30);
                border-radius: 50px;  /* half of height for oval shape */
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,80);
                color: black;
            }
            QPushButton:pressed {
                background-color: rgba(255,255,255,150);
            }
        """)
        button.setCursor(Qt.PointingHandCursor)
        # Glow/Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setColor(Qt.white)
        shadow.setOffset(0)
        button.setGraphicsEffect(shadow)

    def fade_in_ui(self, duration=600, delay=200):
        # Sequential animation group
        seq_group = QSequentialAnimationGroup(self)

        # Fade-in user label
        anim_label = QPropertyAnimation(self.user_label, b"windowOpacity")
        anim_label.setDuration(duration)
        anim_label.setStartValue(0.0)
        anim_label.setEndValue(1.0)
        seq_group.addAnimation(anim_label)

        # Fade-in buttons one by one
        for btn in self.buttons:
            anim_btn = QPropertyAnimation(btn, b"windowOpacity")
            anim_btn.setDuration(duration)
            anim_btn.setStartValue(0.0)
            anim_btn.setEndValue(1.0)
            seq_group.addPause(delay)  # stagger
            seq_group.addAnimation(anim_btn)

        # Keep reference to prevent garbage collection
        self._seq_anim = seq_group
        seq_group.start()

    def update_user_label(self, user_name):
        if user_name:
            self.user_label.setText(f"Welcome, {user_name}")
        else:
            self.user_label.setText("Welcome, ")
        
    def select_user(self):
        print("User selected!", self.user_button.text())    

    def launch_media(self):
        self.main_window.chromium.launch(DEFAULT_MEDIA_URL)

    def start_ride(self):
        self.main_window.set_state(AppState.RIDE_ACTIVE)
