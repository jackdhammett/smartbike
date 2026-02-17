from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QSequentialAnimationGroup, QPropertyAnimation
from PyQt5.QtGui import QColor
from App.StateManager import AppState
from App.config import DEFAULT_MEDIA_URL, SERVICES

class RideSetupScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background: transparent;")

        layout = QVBoxLayout()
        layout.setSpacing(40)
        layout.setContentsMargins(100, 100, 100, 100)
        layout.setAlignment(Qt.AlignCenter)

        # Label above user selection
        self.user_label = QLabel("Welcome, ")
        self.user_label.setAlignment(Qt.AlignCenter)
        self.user_label.setStyleSheet("color: #ffffff; font-size: 42px; background: transparent; font-weight: 300; letter-spacing: 1px;")
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
        self.launch_youtube_btn = QPushButton("Youtube")
        self.launch_youtube_btn.clicked.connect(self.launch_youtube)
        self.style_tile_button(self.launch_youtube_btn)
        button_layout.addWidget(self.launch_youtube_btn)

        # Launch Media button
        self.launch_hulu_btn = QPushButton("Hulu")
        self.launch_hulu_btn.clicked.connect(self.launch_hulu)
        self.style_tile_button(self.launch_hulu_btn)
        button_layout.addWidget(self.launch_hulu_btn)


        # Launch Media button
        self.launch_hbo_btn = QPushButton("HBO")
        self.launch_hbo_btn.clicked.connect(self.launch_hbo)
        self.style_tile_button(self.launch_hbo_btn)
        button_layout.addWidget(self.launch_hbo_btn)


        # Launch Media button
        self.launch_netflix_btn = QPushButton("Netflix")
        self.launch_netflix_btn.clicked.connect(self.launch_netflix)
        self.style_tile_button(self.launch_netflix_btn)
        button_layout.addWidget(self.launch_netflix_btn)


        # Store buttons for fade-in animation
        self.buttons = [self.start_ride_btn, self.launch_hbo_btn, self.launch_hulu_btn, self.launch_netflix_btn, self.launch_youtube_btn]
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.user_label.setWindowOpacity(0.0)
        for btn in self.buttons:
            btn.setWindowOpacity(0.0)

    def style_tile_button(self, button: QPushButton):
        button.setFixedSize(280, 60)
        button.setStyleSheet("""
            QPushButton {
                color: #ffffff;
                font-size: 18px;
                font-weight: 500;
                background-color: #0f1a3a;
                border: 2px solid #1a2847;
                border-radius: 8px;
                padding: 0px;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #1a2847;
                border: 2px solid #00d9ff;
                color: #00d9ff;
            }
            QPushButton:pressed {
                background-color: #2d3e5f;
                border: 2px solid #00d9ff;
            }
        """)
        button.setCursor(Qt.PointingHandCursor)
        # Subtle shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setColor(QColor(0, 217, 255, 40))
        shadow.setOffset(0, 2)
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

    def launch_youtube(self):
        self.main_window.hide_background()
        self.main_window.chromium.launch(SERVICES["youtube"])

    def launch_hulu(self):
        self.main_window.hide_background()
        self.main_window.chromium.launch(SERVICES["hulu"])
        
    def launch_netflix(self):
        self.main_window.hide_background()
        self.main_window.chromium.launch(SERVICES["netflix"])

    def launch_hbo(self):
        self.main_window.hide_background()
        self.main_window.chromium.launch(SERVICES["hbo"])
        
    def start_ride(self):
        self.main_window.set_state(AppState.RIDE_ACTIVE)
