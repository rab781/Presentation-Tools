# Configuration Reference

The application behavior is controlled by `user_config.json` in the project root. You customize this file to adjust the tool to your environment and preferences.

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
