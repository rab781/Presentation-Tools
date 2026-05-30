# API Reference

The Presentation Control Tool exposes several classes and a configuration manager that you can use programmatically to extend or integrate the tool into other systems.

## `ConfigManager`

The `ConfigManager` handles user configuration with persistence. It reads and writes to `user_config.json`. A singleton instance named `config_manager` is exported by the `config` module.

### Methods

-   **`get(key: str, default=None) -> Any`**
    Retrieves a configuration value.
    -   `key`: The configuration key.
    -   `default`: The value to return if the key is not found.

-   **`set(key: str, value: Any)`**
    Sets a configuration value and automatically saves it to `user_config.json`.
    -   `key`: The configuration key.
    -   `value`: The value to store.

-   **`get_mode() -> OperationMode`**
    Retrieves the current operation mode (Gesture, Voice, or Hybrid) as an `OperationMode` enum.

-   **`set_mode(mode: OperationMode)`**
    Sets the operation mode.

### Available Configuration Keys

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

### Example

```python
from config import config_manager, OperationMode

# Get the current mode
current_mode = config_manager.get_mode()

# Set a higher debounce time for slower command execution
config_manager.set("debounce_time", 1.0)

# Switch to voice-only mode
config_manager.set_mode(OperationMode.VOICE_ONLY)
```

## `PresentationController`

The `PresentationController` manages keyboard simulation and application-specific commands. It runs in a background thread to process commands asynchronously.

### Methods

-   **`__init__(debounce_time=0.5)`**
    Initializes the controller.

-   **`start()`**
    Starts the controller thread.

-   **`stop()`**
    Stops the controller thread.

-   **`send_command(command: str, source: str = "manual")`**
    Adds a command to the execution queue.

-   **`detect_active_application() -> str`**
    Detects the currently active presentation application and returns its profile name (e.g., `"powerpoint"`, `"google_slides"`, `"universal"`).

-   **`set_application(app_name: str)`**
    Manually sets the active application profile.

-   **`auto_detect_application()`**
    Automatically detects and sets the application profile.

-   **`get_available_commands() -> list`**
    Returns a list of available commands for the current application profile.

### Example

```python
from controller import PresentationController

controller = PresentationController()
controller.start()

# Manually set the profile
controller.set_application("powerpoint")

# Send a command to go to the next slide
controller.send_command("next", source="script")

# Clean up
controller.stop()
```