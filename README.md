# Presentation Control Tool

> Control your presentations hands-free using hand gestures and voice commands.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Exists

Clickers get lost, batteries die, and holding a device limits your expressiveness during a presentation. The Presentation Control Tool solves this pain point. You turn your webcam and microphone into a universal controller, and you navigate slides fluidly without breaking your flow.

## Quick Start

You clone the repository, install dependencies, and run the main application.

```bash
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools
pip install -r requirements.txt
python main.py
```

```python
from config import config_manager, OperationMode

# You configure the application programmatically
config_manager.set_mode(OperationMode.GESTURE_ONLY)
config_manager.set("debounce_time", 1.0)
```

## Tutorials

### Installation

**Prerequisites**: You need Python 3.8+ and a working webcam and microphone.

First, you set up a virtual environment to isolate your dependencies.

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Next, you install the required packages. If you use macOS or Linux and see an error about `pywin32`, you ignore it, as it is a Windows-only package.

```bash
pip install -r requirements.txt
```

> **Tip**: If you see `pip install pyaudio` fail on Windows, you install the pre-compiled binary instead:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### Basic Usage

You start the controller by running the main script. You stand 0.5 to 2 meters from your webcam, open your presentation (like PowerPoint or Google Slides), and use gestures or voice to navigate.

```bash
python main.py
```

- You **swipe right** to go to the next slide.
- You say **"previous"** to go back.

## How-To Guides

### How to Configure Offline Voice Recognition

You configure offline voice commands in Indonesian using a Vosk model.

1. You create a `models` directory in the project root.
2. You download the [Vosk Indonesian Small Model](https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip).
3. You extract the contents into the `models` directory.
4. You configure offline mode by updating `user_config.json` with `"offline_mode": true`.

### How to Calibrate Your Setup

If you experience trouble with gesture detection or voice recognition, you run the calibration wizard. The wizard tests your setup and provides recommended settings.

```bash
python main.py --calibrate
```

## Reference

### Configuration

You customize the application behavior by creating or editing `user_config.json` in the project root.

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

### Hand Gestures

| Gesture | Command | Action |
|---------|---------|--------|
| 👉 Swipe Right | Next | Next slide |
| 👈 Swipe Left | Previous | Previous slide |
| ✋ Open Palm | Pause | Pause/Blackout |
| ✊ Closed Fist | Play | Resume |
| 👍 Thumbs Up | First | First slide |
| 👎 Thumbs Down | Last | Last slide |
| ✌️ Peace Sign | Blackout | Black screen |

### Voice Commands

You use English or Indonesian commands.

- **Navigation**: "next", "previous", "back", "first", "last", "start", "end"
- **Control**: "pause", "stop", "play", "resume", "exit", "quit"
- **Indonesian**: "lanjut", "berikutnya", "kembali", "sebelumnya", "pertama", "terakhir", "berhenti", "jeda", "lanjutkan", "mulai", "keluar"

### Keyboard Controls

While you run the application, you press these keys to control the tool:

| Key | Function |
|-----|----------|
| **G** | Switch to Gesture Only mode |
| **V** | Switch to Voice Only mode |
| **H** | Switch to Hybrid mode (default) |
| **C** | Run calibration wizard |
| **A** | Auto-detect active application manually |
| **P** | Pause/Resume detection |
| **ESC** | Exit application |

### API Reference

You use the configuration manager programmatically.

```python
from config import config_manager, OperationMode

# You get a value
mode = config_manager.get_mode()

# You set a value (automatically saves to user_config.json)
config_manager.set_mode(OperationMode.GESTURE_ONLY)
config_manager.set("debounce_time", 1.0)
```

## Explanation

### Application Detection

The Presentation Control Tool automatically detects your active presentation software. It monitors the active window title and process name, and maps your gestures or voice commands to the specific keyboard shortcuts required by that application (e.g., PowerPoint, Google Slides, PDF viewers).

## Contributing

Contributions are welcome! You submit a Pull Request by following these steps:

1. You fork the project.
2. You create your feature branch (`git checkout -b feature/AmazingFeature`).
3. You commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. You push to the branch (`git push origin feature/AmazingFeature`).
5. You open a Pull Request.

## License

MIT © [Presentation Control Tool](https://github.com/rab781/Presentation-Tools)
