import json
import os
from pathlib import Path
from datetime import datetime


class RideHistoryService:
    """Service for managing ride history data"""
    
    def __init__(self, data_file='Data/ride_history.json'):
        self.data_file = data_file
        self.rides = []
        self.ensure_file_exists()
        self.load_rides()
    
    def ensure_file_exists(self):
        """Create ride_history.json if it doesn't exist"""
        if not os.path.exists(self.data_file):
            # Create with sample data (distance in miles, avg_speed in mph)
            initial_data = {
                "rides": [
                    {"user": "Jack", "distance_miles": 19.4, "avg_speed": 23.5, "calories": 325, "duration_minutes": 45, "date": "2026-02-10"},
                    {"user": "Jack", "distance_miles": 17.7, "avg_speed": 23.8, "calories": 275, "duration_minutes": 38, "date": "2026-02-08"},
                    {"user": "Jack", "distance_miles": 19.4, "avg_speed": 22.4, "calories": 380, "duration_minutes": 52, "date": "2026-02-05"},
                ]
            }
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def load_rides(self):
        """Load all rides from file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.rides = data.get('rides', [])
        except (json.JSONDecodeError, FileNotFoundError):
            self.rides = []
    
    def save_rides(self):
        """Save rides to file"""
        data = {"rides": self.rides}
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_ride(self, user_name, distance_miles, avg_speed, calories, duration_minutes):
        """Add a new ride record
        
        Args:
            user_name: Name of the user
            distance_miles: Ride distance in miles
            avg_speed: Average speed in mph
            calories: Calories burned
            duration_minutes: Ride duration in minutes
        """
        ride = {
            "user": user_name,
            "distance_miles": distance_miles,
            "avg_speed": avg_speed,
            "calories": calories,
            "duration_minutes": duration_minutes,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.rides.append(ride)
        self.save_rides()
        return ride
    
    def get_all_rides(self):
        """Get all rides sorted by duration (longest first)"""
        return sorted(self.rides, 
                     key=lambda x: x.get('duration_minutes', 0), 
                     reverse=True)
    
    def get_top_rides(self, limit=5):
        """Get top N longest rides
        
        Args:
            limit: Number of rides to return
        
        Returns:
            List of ride dictionaries
        """
        all_rides = self.get_all_rides()
        return all_rides[:limit]
    
    def get_user_rides(self, user_name):
        """Get all rides for a specific user
        
        Args:
            user_name: Name of the user
        
        Returns:
            List of ride dictionaries for that user
        """
        user_rides = [r for r in self.rides if r.get('user') == user_name]
        return sorted(user_rides, 
                     key=lambda x: x.get('duration_minutes', 0), 
                     reverse=True)
    
    def get_user_best_ride(self, user_name):
        """Get longest ride for a specific user
        
        Args:
            user_name: Name of the user
        
        Returns:
            Best ride dictionary or None
        """
        user_rides = self.get_user_rides(user_name)
        return user_rides[0] if user_rides else None
    
    def get_formatted_rides(self, rides):
        """Convert ride data to format suitable for leaderboard
        
        Args:
            rides: List of ride dictionaries
        
        Returns:
            List of formatted dicts with 'name', 'distance_miles', 'avg_speed', 'calories', 'duration_minutes'
        """
        return [
            {
                'name': r.get('user', 'Unknown'),
                'distance_miles': r.get('distance_miles', 0),
                'avg_speed': r.get('avg_speed', 0),
                'calories': r.get('calories', 0),
                'duration_minutes': r.get('duration_minutes', 0)
            }
            for r in rides
        ]
