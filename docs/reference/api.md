# Reference: ConfigManager API

The `ConfigManager` class in `config.py` acts as a singleton that manages configuration state and automatic persistence to the local `user_config.json` file.

To interact with the configuration programmatically, import the global instance:

```python
from config import config_manager, OperationMode
```

## Methods

### `get(key: str, default: any = None) -> any`

Retrieves a configuration value.

**Parameters:**
- `key`: The string identifier for the configuration setting (e.g., `"debounce_time"`).
- `default`: An optional fallback value returned if the key does not exist.

**Returns:** The configured value or the default.

---

### `set(key: str, value: any)`

Updates a configuration value and immediately saves it to disk (`user_config.json`).

**Parameters:**
- `key`: The string identifier for the configuration setting.
- `value`: The new value to store.

**Example:**
```python
config_manager.set("sound_effects", False)
```

---

### `get_mode() -> OperationMode`

Retrieves the currently active operation mode as an `OperationMode` enum instance.

**Returns:** `OperationMode.GESTURE_ONLY`, `OperationMode.VOICE_ONLY`, or `OperationMode.HYBRID`.

---

### `set_mode(mode: OperationMode)`

Updates the active operation mode and saves it to disk.

**Parameters:**
- `mode`: An instance of the `OperationMode` enum.

**Example:**
```python
from config import config_manager, OperationMode

config_manager.set_mode(OperationMode.VOICE_ONLY)
```

---

### `load_config()`

Force-reloads the configuration from `user_config.json`, overwriting any current in-memory settings. Called automatically during initialization.

---

### `save_config()`

Force-saves the current in-memory dictionary to `user_config.json`. Called automatically by the `set()` and `set_mode()` methods.