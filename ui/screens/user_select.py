from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect, QInputDialog
from PyQt5.QtCore import Qt, QSequentialAnimationGroup, QPropertyAnimation
from App.StateManager import AppState
import json
import os

class UserSelectScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.users_file = "Data/Users.json"
        self.selected_user = None

        layout = QVBoxLayout()

        title = QLabel("Select User")
        title.setObjectName("title")
        title.setStyleSheet("color: white; background: transparent; font-size: 32px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # User buttons layout
        self.users_layout = QVBoxLayout()
        self.users_layout.setAlignment(Qt.AlignCenter)
        self.users_layout.setSpacing(15)
        layout.addLayout(self.users_layout)

        # Add user button
        self.add_user_button = QPushButton("+ Add User")
        self.add_user_button.clicked.connect(self.add_user)
        self.style_tile_button(self.add_user_button)
        layout.addWidget(self.add_user_button, alignment=Qt.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)
        
        self.load_users()

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                users = json.load(f)
        else:
            users = []
        
        # Clear existing user buttons
        while self.users_layout.count():
            self.users_layout.takeAt(0).widget().deleteLater()
        
        # Create button for each user
        for user in users:
            button = QPushButton(user["name"])
            button.clicked.connect(lambda checked, u=user["name"]: self.select_user(u))
            self.style_tile_button(button)
            self.users_layout.addWidget(button, alignment=Qt.AlignCenter)

    def add_user(self):
        name, ok = QInputDialog.getText(self, "Add User", "Enter user name:")
        if ok and name.strip():
            self.save_user(name.strip())
            self.load_users()

    def save_user(self, name):
        users = []
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                users = json.load(f)
        
        if not any(u["name"] == name for u in users):
            users.append({"name": name, "weight": 0})
            with open(self.users_file, "w") as f:
                json.dump(users, f, indent=2)

    def select_user(self, user_name):
        self.main_window.selected_user = user_name
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