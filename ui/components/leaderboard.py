from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFontMetrics


class LeaderboardEntry(QFrame):
    """Individual leaderboard entry row - horizontal layout"""
    def __init__(self, rank, name, distance_miles, avg_speed, calories, duration_minutes):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(15, 26, 58, 150);
                border: 1px solid #1a2847;
                border-radius: 6px;
                padding: 8px;
                margin: 3px 0px;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(10, 6, 10, 6)
        
        # Rank
        rank_label = QLabel(f"#{rank}")
        rank_label.setStyleSheet("color: #00d9ff; font-size: 13px; font-weight: 700;")
        rank_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        rank_label.setMinimumWidth(self._calculate_width(rank_label, "##"))
        layout.addWidget(rank_label)
        
        # Add spacing after rank to move name right
        layout.addSpacing(15)
        
        # Name
        name_label = QLabel(name)
        name_label.setStyleSheet("color: #ffffff; font-size: 13px; font-weight: 500;")
        name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        name_label.setMinimumWidth(self._calculate_width(name_label, "Username"))
        layout.addWidget(name_label)
        
        # Distance
        distance_label = QLabel(f"{distance_miles:.1f}mi")
        distance_label.setStyleSheet("color: #b0b0b0; font-size: 12px;")
        distance_label.setAlignment(Qt.AlignCenter)
        distance_label.setMinimumWidth(self._calculate_width(distance_label, "999.9mi"))
        layout.addWidget(distance_label)
        
        # Avg Speed
        speed_label = QLabel(f"{avg_speed:.1f}mph")
        speed_label.setStyleSheet("color: #b0b0b0; font-size: 12px;")
        speed_label.setAlignment(Qt.AlignCenter)
        speed_label.setMinimumWidth(self._calculate_width(speed_label, "999.9mph"))
        layout.addWidget(speed_label)
        
        # Add spacing before calories to move it left
        layout.addSpacing(15)
        
        # Calories
        calories_label = QLabel(f"{calories}cal")
        calories_label.setStyleSheet("color: #b0b0b0; font-size: 12px;")
        calories_label.setAlignment(Qt.AlignCenter)
        calories_label.setMinimumWidth(self._calculate_width(calories_label, "9999cal"))
        layout.addWidget(calories_label)
        
        # Time
        time_label = QLabel(f"{duration_minutes}min")
        time_label.setStyleSheet("color: #b0b0b0; font-size: 12px;")
        time_label.setAlignment(Qt.AlignCenter)
        time_label.setMinimumWidth(self._calculate_width(time_label, "999min"))
        layout.addWidget(time_label)
        
        self.setLayout(layout)
    
    @staticmethod
    def _calculate_width(label, sample_text):
        """Calculate required width for text with padding"""
        metrics = QFontMetrics(label.font())
        return metrics.width(sample_text) + 10  # 10px padding


class Leaderboard(QWidget):
    """Leaderboard widget displaying top rides"""
    rides_updated = pyqtSignal()  # Signal for external updates
    
    def __init__(self):
        super().__init__()
        self.rides_data = []
        self.max_entries = 5  # Show top 5 by default
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = QLabel("Longest Rides")
        title.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: 600; letter-spacing: 0.5px;")
        layout.addWidget(title)
        
        # Column headers
        headers_layout = QHBoxLayout()
        headers_layout.setSpacing(0)
        headers_layout.setContentsMargins(10, 6, 10, 6)
        
        # Headers with dynamic widths based on sample data
        headers = [
            ("Rank", "##", Qt.AlignLeft | Qt.AlignVCenter),
            ("Name", "Username", Qt.AlignLeft | Qt.AlignVCenter),
            ("Distance", "999.9mi", Qt.AlignCenter),
            ("Avg Speed", "999.9mph", Qt.AlignCenter),
            ("Calories", "9999cal", Qt.AlignCenter),
            ("Time", "999min", Qt.AlignCenter)
        ]
        
        for i, (header_text, sample_text, alignment) in enumerate(headers):
            label = QLabel(header_text)
            label.setStyleSheet("color: #00d9ff; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
            metrics = QFontMetrics(label.font())
            label.setMinimumWidth(metrics.width(sample_text) + 10)
            label.setAlignment(alignment)
            headers_layout.addWidget(label)
            
            # Add spacing to match data rows
            if i == 0:  # After Rank
                headers_layout.addSpacing(15)
            elif i == 3:  # After Avg Speed, before Calories
                headers_layout.addSpacing(15)
        
        layout.addLayout(headers_layout)
        
        # Scrollable area for entries
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: transparent;
                width: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #1a2847;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #00d9ff;
            }
        """)
        
        # Container for entries
        self.entries_container = QWidget()
        self.entries_layout = QVBoxLayout()
        self.entries_layout.setSpacing(3)
        self.entries_layout.setContentsMargins(0, 0, 0, 0)
        self.entries_layout.addStretch()
        self.entries_container.setLayout(self.entries_layout)
        
        scroll_area.setWidget(self.entries_container)
        layout.addWidget(scroll_area)
        
        self.setLayout(layout)
    
    def load_rides(self, rides_list):
        """Load ride data and display in leaderboard
        
        Args:
            rides_list: List of dicts with keys: name, distance_km, avg_speed, calories, duration_minutes
        """
        self.rides_data = rides_list
        self.refresh_display()
    
    def refresh_display(self):
        """Refresh the leaderboard display"""
        # Clear existing entries
        while self.entries_layout.count() > 1:  # Keep the stretch
            item = self.entries_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Sort by distance descending (longest rides first)
        sorted_rides = sorted(self.rides_data, 
                            key=lambda x: x.get('distance_miles', 0), 
                            reverse=True)
        
        # Add top entries
        for rank, ride in enumerate(sorted_rides[:self.max_entries], 1):
            entry = LeaderboardEntry(
                rank=rank,
                name=ride.get('name', 'Unknown'),
                distance_miles=ride.get('distance_miles', 0),
                avg_speed=ride.get('avg_speed', 0),
                calories=ride.get('calories', 0),
                duration_minutes=ride.get('duration_minutes', 0)
            )
            # Insert before the stretch
            self.entries_layout.insertWidget(rank - 1, entry)
        
        self.rides_updated.emit()
    
    def add_ride(self, name, distance_miles, avg_speed, calories, duration_minutes):
        """Add a new ride to the leaderboard
        
        Args:
            name: User name
            distance_miles: Ride distance in miles
            avg_speed: Average speed in mph
            calories: Calories burned
            duration_minutes: Ride duration in minutes
        """
        self.rides_data.append({
            'name': name,
            'distance_miles': distance_miles,
            'avg_speed': avg_speed,
            'calories': calories,
            'duration_minutes': duration_minutes
        })
        self.refresh_display()
    
    def set_max_entries(self, count):
        """Set maximum number of entries to display"""
        self.max_entries = count
        self.refresh_display()

