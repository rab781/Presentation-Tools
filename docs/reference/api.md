# Reference: API

The Presentation Control Tool exposes a configuration manager that allows you to programmatically read and update settings. The `ConfigManager` is a singleton instance that automatically persists state to a local `user_config.json` file.

## `config_manager`

The singleton instance of `ConfigManager` used to manage application settings.

### Import

```python
from config import config_manager, OperationMode
```

### Methods

#### `get(key: str, default=None)`

Retrieves a configuration value.

- **Parameters:**
  - `key` (`str`): The configuration key to retrieve (e.g., `"debounce_time"`).
  - `default` (`Any`, optional): The default value to return if the key is not found.
- **Returns:** The configuration value, or the default if not found.

#### `set(key: str, value: Any)`

Sets a configuration value and automatically saves it to `user_config.json`.

- **Parameters:**
  - `key` (`str`): The configuration key to set.
  - `value` (`Any`): The value to assign to the key.

#### `get_mode() -> OperationMode`

Retrieves the current operation mode.

- **Returns:** An `OperationMode` enum value (`GESTURE_ONLY`, `VOICE_ONLY`, or `HYBRID`).

#### `set_mode(mode: OperationMode)`

Sets the current operation mode and automatically saves it to `user_config.json`.

- **Parameters:**
  - `mode` (`OperationMode`): The new operation mode enum value.

#### `load_config()`

Explicitly reloads the configuration from `user_config.json`. This is called automatically during initialization.

#### `save_config()`

Explicitly saves the current configuration state to `user_config.json`. This is called automatically when using `set()` or `set_mode()`.

## `OperationMode` Enum

Defines the available operation modes for the application.

- `OperationMode.GESTURE_ONLY`: ("gesture") Enables only hand gesture detection.
- `OperationMode.VOICE_ONLY`: ("voice") Enables only voice command recognition.
- `OperationMode.HYBRID`: ("hybrid") Enables both gesture and voice detection.
