# API Reference: ConfigManager

The `config_manager` is a singleton instance of the `ConfigManager` class that manages user configuration with persistence to `user_config.json`. You use it to programmatically get and set configuration values within the Presentation Control Tool.

## Import

```python
from config import config_manager, OperationMode
```

## Methods

### `get(key, default=None)`

Retrieves a configuration value.

- **Parameters:**
  - `key` (str): The configuration key to look up.
  - `default` (any, optional): The value to return if the key is not found. Defaults to `None`.
- **Returns:**
  - The value associated with the key, or the default value.

**Example:**

```python
debounce = config_manager.get("debounce_time", 0.5)
print(f"Debounce time is {debounce} seconds")
```

### `set(key, value)`

Sets a configuration value and automatically saves it to `user_config.json`.

- **Parameters:**
  - `key` (str): The configuration key to set.
  - `value` (any): The new value.
- **Returns:**
  - `None`

**Example:**

```python
config_manager.set("sound_effects", False)
```

### `get_mode()`

Retrieves the current operation mode as an `OperationMode` enum.

- **Returns:**
  - An instance of the `OperationMode` enum (`GESTURE_ONLY`, `VOICE_ONLY`, or `HYBRID`).

**Example:**

```python
current_mode = config_manager.get_mode()
if current_mode == OperationMode.GESTURE_ONLY:
    print("Only responding to gestures")
```

### `set_mode(mode)`

Sets the operation mode and automatically saves it to `user_config.json`.

- **Parameters:**
  - `mode` (OperationMode): The new mode.
- **Returns:**
  - `None`

**Example:**

```python
config_manager.set_mode(OperationMode.HYBRID)
```

## Enums

### `OperationMode`

An enumeration representing the available operation modes.

| Name | Value | Description |
|------|-------|-------------|
| `GESTURE_ONLY` | `"gesture"` | Only process hand gestures. |
| `VOICE_ONLY` | `"voice"` | Only process voice commands. |
| `HYBRID` | `"hybrid"` | Process both gestures and voice commands. |
