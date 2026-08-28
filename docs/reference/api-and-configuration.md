# Reference: API and Configuration

This reference details the available configuration options, recognized hand gestures, supported voice commands, and keyboard shortcuts for the Presentation Control Tool. It also provides the programmatic API for the `ConfigManager`.

## Configuration Options

Customize the application behavior by creating or editing `user_config.json` in the project root. The application automatically loads this file on startup.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | `string` | `"hybrid"` | Operation mode: `"gesture"`, `"voice"`, or `"hybrid"`. |
| `gesture_sensitivity`| `float` | `0.7` | Confidence threshold for gesture detection (0.0 - 1.0). |
| `voice_sensitivity` | `float` | `0.6` | Confidence threshold for voice detection (0.0 - 1.0). |
| `debounce_time` | `float` | `0.5` | Minimum delay between commands in seconds. |
| `camera_index` | `integer`| `0` | Webcam index (0 for default, 1 for external). |
| `show_ui` | `boolean`| `true` | Display the real-time camera overlay and status. |
| `sound_effects` | `boolean`| `true` | Play audio feedback when you issue a command. |
| `offline_mode` | `boolean`| `false` | Use local Vosk model for voice recognition instead of Google. |
| `language` | `string` | `"both"` | Active language: `"english"`, `"indonesian"`, or `"both"`. |

## Hand Gestures

The following table maps physical hand gestures to their corresponding presentation commands. Ensure your hand is clearly visible to the webcam.

| Gesture | Command | Action |
|---------|---------|--------|
| 👉 Swipe Right | Next | Next slide |
| 👈 Swipe Left | Previous | Previous slide |
| ✋ Open Palm | Pause | Pause/Blackout |
| ✊ Closed Fist | Play | Resume |
| 👍 Thumbs Up | First | First slide |
| 👎 Thumbs Down | Last | Last slide |
| ✌️ Peace Sign | Blackout | Black screen |

## Voice Commands

The tool recognizes both English and Indonesian commands. Ensure your microphone is active and you speak clearly.

### Navigation

- **English**: "next", "previous", "back", "first", "last", "start", "end"
- **Indonesian**: "lanjut", "berikutnya", "kembali", "sebelumnya", "pertama", "terakhir"

### Control

- **English**: "pause", "stop", "play", "resume", "exit", "quit"
- **Indonesian**: "berhenti", "jeda", "lanjutkan", "mulai", "keluar"

## Keyboard Controls

While the application is running, use these keyboard shortcuts to modify its state without stopping the script. Ensure the webcam preview window is active when pressing keys.

| Key | Function |
|-----|----------|
| **G** | Switch to Gesture Only mode |
| **V** | Switch to Voice Only mode |
| **H** | Switch to Hybrid mode (default) |
| **C** | Run calibration wizard |
| **A** | Auto-detect active application manually |
| **P** | Pause/Resume detection |
| **ESC** | Exit application |

## Python API Reference

You can interact with the tool's configuration programmatically by importing the `config_manager` singleton. This is useful if you are integrating the controller into another Python application.

### `ConfigManager`

The `ConfigManager` handles loading, saving, and updating the application state. It automatically persists changes to `user_config.json`.

```python
from config import config_manager, OperationMode

# Get the current operation mode
current_mode = config_manager.get_mode()
print(f"Current mode is: {current_mode.value}")

# Set a new operation mode
config_manager.set_mode(OperationMode.GESTURE_ONLY)

# Get an arbitrary configuration value with a fallback default
debounce = config_manager.get("debounce_time", 0.5)

# Update a configuration value (this automatically saves to disk)
config_manager.set("debounce_time", 1.0)
```
