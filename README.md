# Presentation Control Tool

> Turn your webcam and microphone into a universal presentation remote to navigate slides hands-free.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Exists

Clickers get lost, batteries die, and holding a device limits your expressiveness during a presentation. The Presentation Control Tool solves this by turning your webcam and microphone into a universal controller. You automatically detect your presentation software and navigate slides fluidly without breaking your flow.

## Quick Start

```bash
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools
pip install -r requirements.txt
python main.py
```

## Installation

**Prerequisites**: Python 3.8+ and a working webcam/microphone.

You create a virtual environment to isolate dependencies:

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

You install the required Python packages:

```bash
pip install -r requirements.txt
```

> **Tip for macOS/Linux users:** The `requirements.txt` file includes `pywin32`, which is a Windows-only package. If `pip` fails when trying to install `pywin32`, you skip that package and install the remaining dependencies normally.

> **Tip for Windows users:** If `pip install pyaudio` fails, you install the pre-compiled binary using `pipwin`:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

## Usage

### Basic Example

You open your presentation in PowerPoint, Google Slides, Canva, or a PDF viewer. Then, you start the controller:

```bash
python main.py
```

You stand 0.5 - 2 meters from your webcam. You control your presentation using hand gestures or voice commands:

- **Swipe your hand right** to go to the next slide.
- **Say "previous"** (or "sebelumnya") to go back.

### Supported Interactions

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

You use either English or Indonesian commands.

- **Navigation**: "next", "previous", "back", "first", "last", "start", "end"
- **Control**: "pause", "stop", "play", "resume", "exit", "quit"
- **Indonesian**: "lanjut", "berikutnya", "kembali", "sebelumnya", "pertama", "terakhir", "berhenti", "jeda", "lanjutkan", "mulai", "keluar"

### Configuration

You customize the application behavior by creating or editing `user_config.json` in the project root.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | `string` | `"hybrid"` | Operation mode: `"gesture"`, `"voice"`, or `"hybrid"` |
| `gesture_sensitivity`| `number` | `0.7` | Confidence threshold for gesture detection (0.0 - 1.0) |
| `voice_sensitivity` | `number` | `0.6` | Confidence threshold for voice detection (0.0 - 1.0) |
| `debounce_time` | `number` | `0.5` | Minimum delay between commands in seconds |
| `camera_index` | `number`| `0` | Webcam index (0 for default, 1 for external) |
| `show_ui` | `boolean`| `true` | Display the real-time camera overlay and status |
| `sound_effects` | `boolean`| `true` | Play audio feedback when a command is recognized |
| `offline_mode` | `boolean`| `false` | Use local Vosk model for voice recognition instead of Google |
| `language` | `string` | `"both"` | Active language: `"english"`, `"indonesian"`, or `"both"` |

### Advanced Usage

#### Offline Voice Recognition

You use a local Vosk model for offline voice commands (Indonesian):

1. Create a `models` directory in the project root.
2. Download the [Vosk Indonesian Small Model](https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip).
3. Extract the contents into the `models` directory.
4. Set `"offline_mode": true` in your `user_config.json`.

#### Keyboard Controls

While the application is running, you press these keys to control the tool:

| Key | Function |
|-----|----------|
| **G** | Switch to Gesture Only mode |
| **V** | Switch to Voice Only mode |
| **H** | Switch to Hybrid mode (default) |
| **C** | Run calibration wizard |
| **A** | Auto-detect active application manually |
| **P** | Pause/Resume detection |
| **ESC** | Exit application |

#### Calibration Wizard

If you experience trouble with gestures or voice recognition, you run the calibration wizard to test your setup and receive recommended settings:

```bash
python main.py --calibrate
```

## API Reference

The project exposes a configuration manager that you use programmatically to manage settings:

```python
from config import config_manager, OperationMode

# Get a value
mode = config_manager.get_mode()

# Set a value (automatically saves to user_config.json)
config_manager.set_mode(OperationMode.GESTURE_ONLY)
config_manager.set("debounce_time", 1.0)
```

For internal modules (`gesture_detector`, `voice_recognizer`, `controller`), you reference the source code docstrings.

## Contributing

You contribute by opening a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT © 2025 Presentation Control Tool
