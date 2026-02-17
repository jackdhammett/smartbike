# SmartBike - Copilot Instructions

## Project Overview

SmartBike is a PyQt5-based GUI application that serves as a media player overlay for stationary bikes. It displays ride metrics (cadence, speed, calories) as a transparent overlay while media plays in the background. The app manages three distinct application states and integrates with Bluetooth Low Energy (BLE) devices for sensor data.

## Architecture

### State-Based Navigation
- **AppState Enum** (`App/StateManager.py`): Defines three states: `USER_SELECT`, `RIDE_SETUP`, `RIDE_ACTIVE`
- **MainWindow** (`ui/main_window.py`): Central hub using `QStackedWidget` to manage screen transitions
  - Each state maps to a corresponding screen widget
  - `set_state()` method handles window flag changes (transparency, layering) based on state

### Key Architectural Patterns

1. **Transparent Overlay Mode** (RIDE_ACTIVE state):
   - Uses Qt flags: `FramelessWindowHint | WindowStaysOnTopHint | Tool`
   - Requires `WA_TranslucentBackground` attribute for transparency
   - Stats box positioned at top-left with semi-transparent background (`rgba(0,0,0,150)`)

2. **Signal-Based Communication**:
   - BLE sensors emit via PyQt signals (e.g., `cadence_updated` signal from `CadenceStub`)
   - Services (metrics) listen to signals and emit processed data back to UI
   - `RideMetrics` transforms cadence → speed (×0.3) and accumulates calories (×0.05)

3. **UI Component Pattern**:
   - Reusable components in `ui/components/` (e.g., `StatTile`)
   - Screens implement animations (fade-in) using `QPropertyAnimation`
   - All text rendered with shadow effects for readability over media

### Module Organization

```
App/          - Application state & configuration
  StateManager.py - Enum defining app states
  config.py      - Constants (APP_NAME, DEFAULT_MEDIA_URL)
  chromium_controller.py - Browser/media process management
Services/     - Data processing & hardware integration
  BLE/         - Bluetooth sensors (currently stubs)
  metrics/     - Ride metrics calculation
ui/           - PyQt5 UI components
  screens/     - Full-screen state widgets (UserSelectScreen, RideSetupScreen, RideActiveScreen)
  components/  - Reusable UI elements
Assets/       - Stylesheets (styles.qss)
Data/         - User data (Users.json)
```

## Running the Application

### Prerequisites
```bash
# Install PyQt5
pip install PyQt5
```

### Start the Application
```bash
python main.py
```

The app starts in fullscreen `USER_SELECT` state.

## Development Conventions

### State Transitions
- **Always use `MainWindow.set_state(AppState.X)`** - never directly call `stack.setCurrentWidget()`
- State transitions handle window flag/transparency changes automatically
- Note: Line 63 in `main_window.py` has a bug—uses string `"RIDE_ACTIVE"` instead of `AppState.RIDE_ACTIVE`

### UI Styling
- QSS stylesheet loaded from `Assets/styles.qss` at startup
- Transparency managed per-state; components inherit parent transparency
- Text colors typically white with drop shadow effects for overlay legibility

### Signal Connections
- Connect signals in `MainWindow.__init__()` (e.g., `cadence.cadence_updated.connect()`)
- Signals are preferred over callbacks for decoupled components
- Service signals should emit simple types (int, dict, str) for easier testing

### File Paths
- Relative paths from project root (e.g., `Assets/styles.qss`, `Data/Users.json`)
- Ensure paths work when running `python main.py` from repo root

### Type Conventions
- Python 3 (no type hints currently used, but compatible)
- Qt signals/slots handle method binding; explicit typing not required for Qt integration
