# Presentation Control Tool

> Control your presentations hands-free using hand gestures and voice commands.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Exists

Clickers get lost, batteries die, and holding a device limits your expressiveness. You need your hands free to present naturally. This tool solves this by turning your webcam and microphone into a universal controller, letting you navigate slides seamlessly without breaking your flow.

## Quick Start

```bash
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools
pip install -r requirements.txt
python main.py
```

## Installation

**Prerequisites**: Python 3.8+ and a working webcam and microphone.

Set up a virtual environment to isolate your project dependencies:

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install -r requirements.txt
```

> **Tip**: If you see an error about `pywin32` on macOS or Linux, ignore it. This package is Windows-only and the tool functions correctly without it.
>
> If `pip install pyaudio` fails on Windows with a build error, install the pre-compiled binary instead:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

## Usage

### Basic Example

Start the controller by running the main script. Stand 0.5 to 2 meters from your webcam, open your presentation software (like PowerPoint or Google Slides), and use gestures or voice to navigate.

```bash
python main.py
```

- **Swipe right** to go to the next slide.
- **Say "previous"** to go back.

### Configuration

Customize the application behavior by creating or editing `user_config.json` in the project root.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | `string` | `"hybrid"` | Operation mode: `"gesture"`, `"voice"`, or `"hybrid"`. |
| `gesture_sensitivity`| `float` | `0.7` | Confidence threshold for gesture detection (0.0 - 1.0). |
| `voice_sensitivity` | `float` | `0.6` | Confidence threshold for voice detection (0.0 - 1.0). |
| `debounce_time` | `float` | `0.5` | Minimum delay between commands in seconds. |
| `camera_index` | `integer`| `0` | Webcam index (`0` for default, `1` for external). |
| `show_ui` | `boolean`| `true` | Display the real-time camera overlay and status. |
| `sound_effects` | `boolean`| `true` | Play audio feedback when you issue a command. |
| `offline_mode` | `boolean`| `false` | Use local Vosk model for voice recognition instead of Google. |
| `language` | `string` | `"both"` | Active language: `"english"`, `"indonesian"`, or `"both"`. |

### Advanced Usage

#### Hand Gestures

| Gesture | Command | Action |
|---------|---------|--------|
| 👉 Swipe Right | Next | Next slide |
| 👈 Swipe Left | Previous | Previous slide |
| ✋ Open Palm | Pause | Pause/Blackout |
| ✊ Closed Fist | Play | Resume |
| 👍 Thumbs Up | First | First slide |
| 👎 Thumbs Down | Last | Last slide |
| ✌️ Peace Sign | Blackout | Black screen |

#### Voice Commands

Use English or Indonesian commands.

- **Navigation**: "next", "previous", "back", "first", "last", "start", "end"
- **Control**: "pause", "stop", "play", "resume", "exit", "quit"
- **Indonesian**: "lanjut", "berikutnya", "kembali", "sebelumnya", "pertama", "terakhir", "berhenti", "jeda", "lanjutkan", "mulai", "keluar"

#### Offline Voice Recognition

Configure offline voice commands in Indonesian using a Vosk model.

1. Create a `models` directory in the project root.
2. Download the [Vosk Indonesian Small Model](https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip).
3. Extract the contents into the `models` directory.

#### Keyboard Controls

While the application runs, press these keys to control the tool:

| Key | Function |
|-----|----------|
| **G** | Switch to Gesture Only mode |
| **V** | Switch to Voice Only mode |
| **H** | Switch to Hybrid mode (default) |
| **C** | Run calibration wizard |
| **A** | Auto-detect active application manually |
| **P** | Pause/Resume detection |
| **ESC** | Exit application |

If gestures or voice commands fail to register, run the calibration wizard. This tests your hardware and provides optimal sensitivity settings for your environment.

```bash
python main.py --calibrate
```

## API Reference

The project exposes a configuration manager that you use programmatically.

```python
from config import config_manager, OperationMode

# Get a value
mode = config_manager.get_mode()

# Set a value (automatically saves to user_config.json)
config_manager.set_mode(OperationMode.GESTURE_ONLY)
config_manager.set("debounce_time", 1.0)
```

For more details on internal modules, refer to the source code docstrings.

## Contributing

You can contribute by submitting a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT © [Presentation Control Tool](https://github.com/rab781/Presentation-Tools)
