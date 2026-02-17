# Theme Switcher

You can easily switch between themes by editing the `Assets/styles.qss` file.

## Current Theme: SPORTY 🔥

**Sporty/Energetic Theme**
- Bold orange/red accent color (#ff3d00)
- High contrast with black backgrounds
- Heavy font weights (700 bold)
- Energetic glowing effects
- Perfect for fitness/performance vibes
- Files affected: `Assets/styles.qss`, `ui/screens/*.py`

## To Switch Back to Dark Luxury Theme

Replace the content of `Assets/styles.qss` with:

```qss
QWidget {
    background-color: #0a0e27;
    color: #ffffff;
    font-family: 'Segoe UI', 'Inter', sans-serif;
}

#title {
    font-size: 42px;
    font-weight: 300;
    letter-spacing: 2px;
    color: #ffffff;
}

#stat_label {
    font-size: 24px;
    color: #a0a8b8;
    font-weight: 300;
}

#stat_value {
    font-size: 48px;
    color: #00d9ff;
    font-weight: 600;
}

QPushButton {
    border: 2px solid #1a2847;
    border-radius: 8px;
    padding: 12px;
    font-weight: 500;
    letter-spacing: 0.5px;
    background-color: #0f1a3a;
    color: #ffffff;
}

QPushButton:hover {
    background-color: #1a2847;
    border: 2px solid #00d9ff;
    color: #00d9ff;
}

QPushButton:pressed {
    background-color: #2d3e5f;
}
```

Then in each screen file (`ui/screens/user_select.py`, `ui/screens/ride_setup.py`, `ui/screens/ride_active.py`), change the button styling back:

### user_select.py style_tile_button():
```python
shadow.setColor(QColor(0, 217, 255, 40))  # Cyan
```

### ride_setup.py welcome label:
```python
self.user_label.setStyleSheet("color: #ffffff; font-size: 42px; background: transparent; font-weight: 300; letter-spacing: 1px;")
```

### ride_setup.py style_tile_button():
```python
shadow.setColor(QColor(0, 217, 255, 40))  # Cyan
```

### ride_active.py stats labels:
```python
lbl.setStyleSheet("color: #00d9ff; font-size: 24px; background: transparent; font-weight: 500;")
shadow.setColor(QColor(0, 217, 255, 80))  # Cyan
```

---

**Comparison:**
- **Dark Luxury**: Subtle, professional, sleek (cyan accents)
- **Sporty**: Bold, energetic, high-energy (orange-red accents)

Choose which one fits your vision better!
