from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from App.StateManager import AppState

class UserSelectScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()

        title = QLabel("Select User")
        title.setObjectName("title")
        title.setStyleSheet("color: white; background: transparent; font-size: 32px;")
        layout.addWidget(title)

        button = QPushButton("John")
        button.setStyleSheet("""
        QPushButton {
            color: white;
            background: transparent;
            border: 2px solid white;
            font-size: 32px;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 50);  /* semi-transparent white */
            color: black;
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 100);
        }
        """)
        button.clicked.connect(self.next_screen)
        layout.addWidget(button)
# User selection as centered oval button
#self.user_button = QPushButton("Select User: John")
#self.style_oval_button(self.user_button)
#self.user_button.clicked.connect(self.select_user)  # handle user selection
#main_layout.addWidget(self.user_button, alignment=Qt.AlignCenter)



        self.setLayout(layout)

    def next_screen(self):
        self.main_window.set_state(AppState.RIDE_SETUP)
    
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