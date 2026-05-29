# Reference

This reference documents the configuration options, gesture mappings, and voice commands available in the Presentation Control Tool.

---

## Configuration

Customize the application behavior by creating or editing `user_config.json` in the project root. The tool automatically reads these settings on startup.

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

## Gesture Commands

By default, the following hand gestures trigger presentation commands. Your hand must be clearly visible and the gesture must be distinct to be recognized.

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

The tool recognizes both English and Indonesian voice commands. The recognition engine listens for these specific keywords and ignores surrounding speech.

### Navigation

| English | Indonesian | Action |
|---------|------------|--------|
| `next`, `start` | `lanjut`, `berikutnya`, `selanjutnya` | Next slide |
| `previous`, `back` | `kembali`, `sebelumnya`, `mundur` | Previous slide |
| `first` | `pertama`, `awal`, `mulai` | First slide |
| `last`, `end` | `terakhir`, `akhir` | Last slide |

### Control

| English | Indonesian | Action |
|---------|------------|--------|
| `pause`, `stop` | `berhenti`, `jeda` | Pause presentation |
| `play`, `resume` | `lanjutkan`, `mulai` | Resume presentation |
| `blackout`, `black` | `hitam`, `gelap` | Black screen |
| `exit`, `quit`, `close` | `keluar`, `tutup` | Exit presentation mode |

## API Example

You can also use the configuration manager programmatically in your own scripts to adjust settings on the fly.

```python
from config import config_manager, OperationMode

# Get the current mode
mode = config_manager.get_mode()

# Set a new value (automatically saves to user_config.json)
config_manager.set_mode(OperationMode.GESTURE_ONLY)
config_manager.set("debounce_time", 1.0)
```