# API Reference

The project exposes a `ConfigManager` singleton that you use to programmatically manage configuration settings.

```python
from config import config_manager, OperationMode

# Get the current operation mode
mode = config_manager.get_mode()

# Set the mode programmatically (automatically saves to user_config.json)
config_manager.set_mode(OperationMode.GESTURE_ONLY)

# Get an arbitrary configuration setting with a fallback default
debounce_time = config_manager.get("debounce_time", 0.5)

# Set an arbitrary configuration setting
config_manager.set("debounce_time", 1.0)
```

For detailed internal behaviors of modules such as `VoiceRecognizer`, `GestureDetector`, and `PresentationController`, refer to the inline docstrings.
