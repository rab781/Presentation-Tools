# API & Command Reference

This document provides a comprehensive list of supported commands, shortcuts, and configuration options.

## Supported Interactions

### Hand Gestures

| Gesture | Command | Action |
|---------|---------|--------|
| 👉 Swipe Right | Next | Next slide |
| 👈 Swipe Left | Previous | Previous slide |
| ✋ Open Palm | Pause | Pause/Blackout |
| ✊ Closed Fist | Play | Resume |
| 👍 Thumbs Up | First | First slide |
| 👎 Thumbs Down | Last | Last slide |
| ✌️ Peace Sign | Blackout | Black screen |

### Voice Commands

You can use either English or Indonesian commands.

- **Navigation**: "next", "previous", "back", "first", "last", "start", "end"
- **Control**: "pause", "stop", "play", "resume", "exit", "quit"
- **Indonesian**: "lanjut", "berikutnya", "kembali", "sebelumnya", "pertama", "terakhir", "berhenti", "jeda", "lanjutkan", "mulai", "keluar"

## Keyboard Shortcuts

While the application is running, you can press these keys to control the tool:

| Key | Function |
|-----|----------|
| **G** | Switch to Gesture Only mode |
| **V** | Switch to Voice Only mode |
| **H** | Switch to Hybrid mode (default) |
| **C** | Run calibration wizard |
| **A** | Auto-detect active application manually |
| **S** | Open application selection menu |
| **1-5** | Set active application manually (1: PowerPoint, 2: Google Slides, 3: PDF Viewer, 4: Canva, 5: Universal) |
| **P** | Pause/Resume detection |
| **ESC** | Exit application |

## Configuration API (`config.py`)

The project exposes a configuration manager (`config_manager`) that handles reading and saving configuration options.

### Default Configuration Options

When running for the first time or if `user_config.json` is missing, the following defaults are used:

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `mode` | `string` | `"hybrid"` | Operation mode: `"gesture"`, `"voice"`, or `"hybrid"`. |
| `gesture_sensitivity`| `float` | `0.7` | Confidence threshold for gesture detection. |
| `voice_sensitivity` | `float` | `0.6` | Confidence threshold for voice detection. |
| `debounce_time` | `float` | `0.5` | Minimum delay (seconds) between commands to avoid accidental double-triggers. |
| `camera_index` | `integer`| `0` | System camera index. `0` is usually the default webcam. |
| `show_ui` | `boolean`| `true` | Display the real-time camera overlay and status UI. |
| `sound_effects` | `boolean`| `true` | Play an audio beep when a command is recognized. |
| `offline_mode` | `boolean`| `false` | If true, uses the local Vosk model for voice recognition instead of Google's online API. |
| `language` | `string` | `"both"` | Active language for voice commands (`"english"`, `"indonesian"`, or `"both"`). |

### `ConfigManager` Methods

You can interact with the configuration manager programmatically:

```python
from config import config_manager, OperationMode

# Get a value (returns None if not found and no default provided)
debounce = config_manager.get("debounce_time", 0.5)

# Set a value (automatically saves to user_config.json)
config_manager.set("sound_effects", False)

# Get the current mode
mode = config_manager.get_mode()

# Set the mode
config_manager.set_mode(OperationMode.GESTURE_ONLY)
```

- `load_config()`: Reads the user's `user_config.json` file if it exists and merges it with `DEFAULT_CONFIG`.
- `save_config()`: Writes the current `self.config` state to `user_config.json`.
- `get(key, default)`: Retrieves a configuration value by key.
- `set(key, value)`: Updates a configuration value and triggers a save.
- `get_mode()`: Retrieves the current operation mode as an `OperationMode` enum.
- `set_mode(mode: OperationMode)`: Sets the current operation mode.
