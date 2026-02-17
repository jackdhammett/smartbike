from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QSequentialAnimationGroup, QPropertyAnimation, QSize
from PyQt5.QtGui import QColor, QPixmap, QIcon
from App.StateManager import AppState
from App.config import DEFAULT_MEDIA_URL, SERVICES
from ui.components.leaderboard import Leaderboard
from Services.ride_history import RideHistoryService

class RideSetupScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background: transparent;")

        # Main vertical layout (top label, then content split)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(40)
        main_layout.setContentsMargins(100, 50, 100, 100)

        # User label at very top - centered across whole screen
        self.user_label = QLabel("Welcome, ")
        self.user_label.setAlignment(Qt.AlignCenter)
        self.user_label.setStyleSheet("color: #ffffff; font-size: 42px; background: transparent; font-weight: 300; letter-spacing: 1px;")
        main_layout.addWidget(self.user_label, alignment=Qt.AlignCenter)

        # Horizontal split layout for content (left and right panels)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(40)

        # LEFT PANEL: Start Ride Button + Future Leaderboard
        left_panel = QVBoxLayout()
        left_panel.setSpacing(20)
        left_panel.setAlignment(Qt.AlignCenter)

        # Large Start Ride button
        self.start_ride_btn = QPushButton("Start Ride")
        self.start_ride_btn.clicked.connect(lambda: main_window.set_state(AppState.RIDE_ACTIVE))
        self.style_large_button(self.start_ride_btn)
        left_panel.addWidget(self.start_ride_btn, alignment=Qt.AlignCenter)

        # Leaderboard widget
        self.leaderboard = Leaderboard()
        self.leaderboard.setMinimumHeight(250)
        self.leaderboard.setMaximumHeight(400)
        left_panel.addWidget(self.leaderboard, alignment=Qt.AlignTop)
        
        # Load ride history data
        self.ride_service = RideHistoryService()
        top_rides = self.ride_service.get_top_rides(limit=5)
        formatted_rides = self.ride_service.get_formatted_rides(top_rides)
        self.leaderboard.load_rides(formatted_rides)

        # RIGHT PANEL: Media Buttons in Rows
        right_panel = QVBoxLayout()
        right_panel.setSpacing(20)
        right_panel.setAlignment(Qt.AlignCenter)

        # Row 1: YouTube and Hulu
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(40)
        row1_layout.setAlignment(Qt.AlignCenter)

        self.launch_youtube_btn = QPushButton()
        self.launch_youtube_btn.clicked.connect(self.launch_youtube)
        self.style_logo_button(self.launch_youtube_btn, "Assets/youtubelogo.png")
        row1_layout.addWidget(self.launch_youtube_btn)

        self.launch_hulu_btn = QPushButton()
        self.launch_hulu_btn.clicked.connect(self.launch_hulu)
        self.style_logo_button(self.launch_hulu_btn, "Assets/hululogo.png")
        row1_layout.addWidget(self.launch_hulu_btn)

        right_panel.addLayout(row1_layout)

        # Row 2: HBO and Netflix
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(40)
        row2_layout.setAlignment(Qt.AlignCenter)

        self.launch_hbo_btn = QPushButton()
        self.launch_hbo_btn.clicked.connect(self.launch_hbo)
        self.style_logo_button(self.launch_hbo_btn, "Assets/hbomaxlogo.png", is_dark=True)
        row2_layout.addWidget(self.launch_hbo_btn)

        self.launch_netflix_btn = QPushButton()
        self.launch_netflix_btn.clicked.connect(self.launch_netflix)
        self.style_logo_button(self.launch_netflix_btn, "Assets/netflixlogo.png")
        row2_layout.addWidget(self.launch_netflix_btn)

        right_panel.addLayout(row2_layout)

        # Add panels to content layout
        content_layout.addLayout(left_panel, 1)
        content_layout.addLayout(right_panel, 1)

        # Add content to main layout
        main_layout.addLayout(content_layout, 1)
        self.setLayout(main_layout)

        # Store buttons for fade-in animation
        self.buttons = [self.start_ride_btn, self.launch_youtube_btn, self.launch_hulu_btn, self.launch_hbo_btn, self.launch_netflix_btn]
        
        self.user_label.setWindowOpacity(0.0)
        for btn in self.buttons:
            btn.setWindowOpacity(0.0)

    def style_large_button(self, button: QPushButton):
        button.setFixedSize(300, 180)
        button.setStyleSheet("""
            QPushButton {
                color: #ffffff;
                font-size: 36px;
                font-weight: 600;
                background-color: #0f1a3a;
                border: 2px solid #1a2847;
                border-radius: 90px;
                padding: 0px;
                letter-spacing: 1px;
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
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(16)
        shadow.setColor(QColor(0, 217, 255, 60))
        shadow.setOffset(0, 4)
        button.setGraphicsEffect(shadow)

    def style_logo_button(self, button: QPushButton, image_path: str, is_dark: bool = False):
        button.setFixedSize(160, 160)
        button.setIconSize(QSize(160, 160))
        pixmap = QPixmap(image_path)
        button.setIcon(QIcon(pixmap))
        
        if is_dark:
            # HBO Max has dark logo, add light background for visibility
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 15);
                    border: 2px solid #2a3a57;
                    border-radius: 80px;
                    padding: 0px;
                }
                QPushButton:hover {
                    border: 2px solid #00d9ff;
                    background-color: rgba(0, 217, 255, 30);
                }
                QPushButton:pressed {
                    border: 2px solid #00d9ff;
                    background-color: rgba(0, 217, 255, 50);
                }
            """)
        else:
            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: 2px solid #1a2847;
                    border-radius: 80px;
                    padding: 0px;
                }
                QPushButton:hover {
                    border: 2px solid #00d9ff;
                    background-color: rgba(0, 217, 255, 20);
                }
                QPushButton:pressed {
                    border: 2px solid #00d9ff;
                    background-color: rgba(0, 217, 255, 40);
                }
            """)
        
        button.setCursor(Qt.PointingHandCursor)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setColor(QColor(0, 217, 255, 40))
        shadow.setOffset(0, 2)
        button.setGraphicsEffect(shadow)

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
    
    def hide_leaderboard(self):
        """Hide the leaderboard widget"""
        self.leaderboard.hide()

    def show_leaderboard(self):
        """Show the leaderboard widget"""
        self.leaderboard.show()
        
    def select_user(self):
        print("User selected!", self.user_button.text())    

    def launch_youtube(self):
        self.hide_leaderboard()
        self.main_window.hide_background()
        self.main_window.chromium.launch(SERVICES["youtube"])

    def launch_hulu(self):
        self.hide_leaderboard()
        self.main_window.hide_background()
        self.main_window.chromium.launch(SERVICES["hulu"])
        
    def launch_netflix(self):
        self.hide_leaderboard()
        self.main_window.hide_background()
        self.main_window.chromium.launch(SERVICES["netflix"])

    def launch_hbo(self):
        self.hide_leaderboard()
        self.main_window.hide_background()
        self.main_window.chromium.launch(SERVICES["hbo"])
        
    def start_ride(self):
        self.main_window.set_state(AppState.RIDE_ACTIVE)
