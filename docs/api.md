# Configuration API Reference

This document provides a comprehensive reference for the configuration components of the Presentation Control Tool. You use these components to programmatically access and modify the application's behavior.

## `ConfigManager` Class

The `ConfigManager` class manages user configuration with persistence, reading from and writing to `user_config.json`. A singleton instance, `config_manager`, is provided for global access.

### Instantiation

You typically import the pre-initialized singleton instance rather than creating a new `ConfigManager`.

```python
from config import config_manager
```

### Methods

#### `load_config(self)`

Loads the configuration from `user_config.json`. If the file exists, it updates the current configuration with the file's contents. If an error occurs, it falls back to default values.

#### `save_config(self)`

Saves the current configuration state to `user_config.json`.

#### `get(self, key, default=None)`

Retrieves a configuration value.

**Parameters:**
- `key` (str): The configuration key to retrieve.
- `default` (any, optional): The value to return if the key is not found. Defaults to `None`.

**Returns:**
- The value associated with the key, or the default value.

**Example:**
```python
debounce_time = config_manager.get("debounce_time", 0.5)
```

#### `set(self, key, value)`

Sets a configuration value and immediately saves the updated configuration to `user_config.json`.

**Parameters:**
- `key` (str): The configuration key to set.
- `value` (any): The new value to assign to the key.

**Example:**
```python
config_manager.set("sound_effects", False)
```

#### `get_mode(self)`

Retrieves the current operation mode.

**Returns:**
- `OperationMode`: The current mode (e.g., `OperationMode.HYBRID`).

**Example:**
```python
current_mode = config_manager.get_mode()
```

#### `set_mode(self, mode: OperationMode)`

Sets the operation mode and automatically saves the configuration.

**Parameters:**
- `mode` (`OperationMode`): The new operation mode to set.

**Example:**
```python
from config import OperationMode
config_manager.set_mode(OperationMode.GESTURE_ONLY)
```

## `OperationMode` Enum

The `OperationMode` enum defines the available interaction modes for the application.

- `OperationMode.GESTURE_ONLY`: ("gesture") Application responds only to hand gestures.
- `OperationMode.VOICE_ONLY`: ("voice") Application responds only to voice commands.
- `OperationMode.HYBRID`: ("hybrid") Application responds to both gestures and voice commands.

## Configuration Dictionaries

The following dictionaries define the default behavior and mappings within the application. You access or update these via the `ConfigManager`.

### `DEFAULT_CONFIG`

The baseline configuration settings used when no custom `user_config.json` is found.

| Key | Type | Default Value | Description |
|-----|------|---------------|-------------|
| `mode` | `string` | `"hybrid"` | The initial operation mode. |
| `gesture_sensitivity` | `float` | `0.7` | Confidence threshold for gestures. |
| `voice_sensitivity` | `float` | `0.6` | Confidence threshold for voice recognition. |
| `debounce_time` | `float` | `0.5` | Minimum seconds between executing consecutive commands. |
| `camera_index` | `int` | `0` | Default camera device index. |
| `show_ui` | `bool` | `True` | Whether to display the visual interface. |
| `sound_effects` | `bool` | `True` | Whether to play auditory feedback on actions. |
| `offline_mode` | `bool` | `False` | Forces local voice processing instead of cloud APIs. |
| `language` | `string` | `"both"` | Active recognition language (`"indonesian"`, `"english"`, or `"both"`). |

### `GESTURE_COMMANDS`

Maps detected hand gestures to logical application commands.

- `SWIPE_RIGHT` -> `"next"`
- `SWIPE_LEFT` -> `"previous"`
- `OPEN_PALM` -> `"pause"`
- `CLOSED_FIST` -> `"play"`
- `THUMB_UP` -> `"first"`
- `THUMB_DOWN` -> `"last"`
- `PEACE_SIGN` -> `"blackout"`

### `VOICE_COMMANDS`

Maps spoken words (in multiple languages) to logical application commands. Note that overlapping keywords (like "lanjut" and "lanjutkan") are handled correctly by the system's length-based substring matching.

- `"next"`: `["next", "lanjut", "berikutnya", "selanjutnya"]`
- `"previous"`: `["previous", "back", "kembali", "sebelumnya", "mundur"]`
- `"first"`: `["first", "start", "pertama", "awal", "mulai"]`
- `"last"`: `["last", "end", "terakhir", "akhir"]`
- `"pause"`: `["pause", "stop", "berhenti", "jeda"]`
- `"play"`: `["play", "resume", "lanjutkan", "mulai"]`
- `"blackout"`: `["black", "blackout", "hitam", "gelap"]`
- `"exit"`: `["exit", "quit", "close", "keluar", "tutup"]`

### `APP_PROFILES`

Maps logical commands (like "next" or "pause") to application-specific keyboard shortcut sequences for various supported platforms (e.g., PowerPoint, Google Slides, Canva).

### `MODE_HOTKEYS`

Maps single-character keyboard inputs to operation mode changes.

- `"g"` -> `OperationMode.GESTURE_ONLY`
- `"v"` -> `OperationMode.VOICE_ONLY`
- `"h"` -> `OperationMode.HYBRID`

### `GESTURE_CONFIG`

Internal tuning parameters for the MediaPipe gesture detection subsystem.

- `min_detection_confidence`: `0.7`
- `min_tracking_confidence`: `0.5`
- `swipe_threshold`: `0.15` (Minimum normalized distance to trigger a swipe)
- `gesture_hold_time`: `0.3` (Seconds a gesture must be held to register)
- `max_hands`: `1`

### `VOICE_CONFIG`

Internal tuning parameters for the speech recognition subsystem (Vosk/Google).

- `energy_threshold`: `4000`
- `dynamic_energy`: `True`
- `pause_threshold`: `0.8`
- `phrase_timeout`: `2`
- `vosk_model_path`: `"./models/vosk-model-small-id-0.22"`

### `UI_CONFIG`

Visual formatting parameters for the OpenCV camera overlay.

- `window_name`: `"Presentation Controller"`
- `show_landmarks`: `True`
- `show_fps`: `True`
- `show_status`: `True`
- `overlay_color`: `(0, 255, 0)`
- `text_color`: `(255, 255, 255)`
- `font_scale`: `0.7`
- `font_thickness`: `2`
