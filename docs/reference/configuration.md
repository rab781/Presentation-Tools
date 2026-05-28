# Reference: Configuration Options

Customize the application behavior by creating or editing `user_config.json` in the project root. The `ConfigManager` automatically persists these settings.

## General Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | `string` | `"hybrid"` | Operation mode: `"gesture"`, `"voice"`, or `"hybrid"`. |
| `gesture_sensitivity`| `float` | `0.7` | Confidence threshold for gesture detection (0.0 - 1.0). |
| `voice_sensitivity` | `float` | `0.6` | Confidence threshold for voice detection (0.0 - 1.0). |
| `debounce_time` | `float` | `0.5` | Minimum delay between commands in seconds to prevent rapid unintended executions. |
| `camera_index` | `integer`| `0` | Webcam index (0 for default, 1 for external). |
| `show_ui` | `boolean`| `true` | Display the real-time camera overlay and status window. |
| `sound_effects` | `boolean`| `true` | Play audio feedback (beeps) when a command is executed. |
| `offline_mode` | `boolean`| `false` | Use the local Vosk model for voice recognition instead of Google Speech Recognition. |
| `language` | `string` | `"both"` | Active language for voice recognition: `"english"`, `"indonesian"`, or `"both"`. |

## Gesture Mappings

The following hand gestures map to specific presentation commands:

| Gesture | Command | Action |
|---------|---------|--------|
| 👉 Swipe Right | `next` | Next slide |
| 👈 Swipe Left | `previous` | Previous slide |
| ✋ Open Palm | `pause` | Pause/Blackout |
| ✊ Closed Fist | `play` | Resume |
| 👍 Thumbs Up | `first` | First slide |
| 👎 Thumbs Down | `last` | Last slide |
| ✌️ Peace Sign | `blackout` | Black screen |

## Voice Commands

You use the following English or Indonesian voice commands:

- **Navigation**: `next`, `previous`, `back`, `first`, `last`, `start`, `end`
- **Control**: `pause`, `stop`, `play`, `resume`, `exit`, `quit`
- **Indonesian Navigation**: `lanjut`, `berikutnya`, `selanjutnya`, `kembali`, `sebelumnya`, `mundur`, `pertama`, `awal`, `mulai`, `terakhir`, `akhir`
- **Indonesian Control**: `berhenti`, `jeda`, `lanjutkan`, `mulai`, `hitam`, `gelap`, `keluar`, `tutup`

## Application Profiles

The tool maps abstract commands (e.g., `next`) to application-specific keyboard shortcuts. Supported profiles include:

- `powerpoint`
- `google_slides`
- `pdf_viewer`
- `canva`
- `universal` (Fallback for unknown applications)

## Keyboard Shortcuts

While the application is running, press these keys to control the tool directly:

| Key | Function |
|-----|----------|
| **G** | Switch to Gesture Only mode |
| **V** | Switch to Voice Only mode |
| **H** | Switch to Hybrid mode (default) |
| **C** | Run calibration wizard |
| **A** | Auto-detect active application manually |
| **S** | Select application profile manually |
| **P** | Pause/Resume detection |
| **ESC** | Exit application |
| **1-5** | Switch to specific application profile (1: PowerPoint, 2: Google Slides, etc.) |
