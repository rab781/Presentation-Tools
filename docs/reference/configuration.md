# Reference: Configuration

The Presentation Control application is configurable via the `ConfigManager` API, which persists settings in the local `user_config.json` file.

The following configuration tables list the default settings stored in `config.py`.

## Core Settings (`DEFAULT_CONFIG`)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `mode` | `string` | `"hybrid"` | Operation mode. Options: `"gesture"`, `"voice"`, `"hybrid"`. |
| `gesture_sensitivity` | `float` | `0.7` | Confidence threshold for gesture detection (0.0 to 1.0). |
| `voice_sensitivity` | `float` | `0.6` | Confidence threshold for voice detection (0.0 to 1.0). |
| `debounce_time` | `float` | `0.5` | Minimum delay between executing commands, in seconds. |
| `camera_index` | `int` | `0` | Device index for the webcam (0 is usually the default camera). |
| `show_ui` | `boolean` | `true` | Display the real-time camera overlay and UI status text. |
| `sound_effects` | `boolean` | `true` | Play audio beep when a command is executed. |
| `offline_mode` | `boolean` | `false` | Enable local Vosk voice recognition instead of Google API. |
| `language` | `string` | `"both"` | Active spoken language. Options: `"indonesian"`, `"english"`, `"both"`. |

## Gesture Detection (`GESTURE_CONFIG`)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `min_detection_confidence` | `float` | `0.7` | Minimum confidence for initial hand detection. |
| `min_tracking_confidence` | `float` | `0.5` | Minimum confidence for continued hand tracking. |
| `swipe_threshold` | `float` | `0.15` | Minimum physical distance required to trigger a swipe. |
| `gesture_hold_time` | `float` | `0.3` | Minimum time (seconds) to hold a gesture for confirmation. |
| `max_hands` | `int` | `1` | Number of hands to track simultaneously. |

## Voice Recognition (`VOICE_CONFIG`)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `energy_threshold` | `int` | `4000` | Minimum audio volume to consider as speech. |
| `dynamic_energy` | `boolean` | `true` | Automatically adjust the energy threshold based on ambient noise. |
| `pause_threshold` | `float` | `0.8` | Seconds of non-speaking audio before a phrase is considered complete. |
| `phrase_timeout` | `int` | `2` | Maximum seconds allowed to complete a spoken phrase. |
| `vosk_model_path` | `string` | `"./models/vosk-model-small-id-0.22"` | Local file path to the extracted Vosk offline model. |

## UI Display (`UI_CONFIG`)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `window_name` | `string` | `"Presentation Controller"` | Title of the OpenCV window. |
| `show_landmarks` | `boolean` | `true` | Draw hand tracking landmarks on the camera feed. |
| `show_fps` | `boolean` | `true` | Display the current Frames Per Second text. |
| `show_status` | `boolean` | `true` | Display the active system status text. |
| `overlay_color` | `tuple` | `(0, 255, 0)` | RGB color (Green) for UI overlays. |
| `text_color` | `tuple` | `(255, 255, 255)` | RGB color (White) for text elements. |
| `font_scale` | `float` | `0.7` | Size multiplier for text rendering. |
| `font_thickness` | `int` | `2` | Thickness (pixels) for text lines. |