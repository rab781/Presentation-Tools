# Presentation Control Tool

> Control your presentations hands-free using hand gestures and voice commands.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10%2B-orange)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Exists

Clickers get lost, batteries die, and holding a device limits your expressiveness during a presentation. The Presentation Control Tool solves this by turning your webcam and microphone into a universal controller. It automatically detects your presentation software (PowerPoint, Google Slides, Canva, or PDF viewers) and lets you navigate slides fluidly without breaking your flow.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools

# Install requirements
pip install -r requirements.txt

# Start the application
python main.py
```

*Note: For Windows users, PyAudio installation can be tricky. See [Installation](#installation) for a reliable method.*

## Installation

**Prerequisites**: Python 3.8+ and a working webcam/microphone.

### 1. Set Up Environment

We recommend creating a virtual environment to isolate dependencies:

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

#### ⚠️ Windows PyAudio Installation

If `pip install pyaudio` fails on Windows, use `pipwin` to install the pre-compiled binary:

```bash
pip install pipwin
pipwin install pyaudio
```

### 3. Optional: Offline Voice Recognition

For offline voice commands (Indonesian), download the Vosk model:

1. Create a `models` directory in the project root.
2. Download the [Vosk Indonesian Small Model](https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip).
3. Extract the contents into the `models` directory.

## Usage

Start the controller by running the main script:

```bash
python main.py
```

### Basic Example: Controlling a Presentation

1. Open your presentation in PowerPoint or Google Slides.
2. Run `python main.py`.
3. Stand 0.5 - 2 meters from your webcam.
4. **Swipe your hand right** to go to the next slide.
5. Say **"previous"** (or "sebelumnya") to go back.

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

You can use either English or Indonesian commands.

- **Navigation**: "next", "previous", "back", "first", "last", "start", "end"
- **Control**: "pause", "stop", "play", "resume", "exit", "quit"
- **Indonesian**: "lanjut", "berikutnya", "kembali", "sebelumnya", "pertama", "terakhir", "berhenti", "jeda", "lanjutkan", "mulai", "keluar"

### Advanced Usage: Calibration and Application Modes

The tool automatically detects your active application and maps commands to the correct keyboard shortcuts.

#### Keyboard Controls

While the application is running, you can press these keys to control the tool:

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

If you are having trouble with gestures or voice recognition, run the calibration wizard to test your setup and receive recommended settings:

```bash
python main.py --calibrate
```

### Configuration

You can customize the application behavior by creating or editing `user_config.json` in the project root.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | `string` | `"hybrid"` | Operation mode: `"gesture"`, `"voice"`, or `"hybrid"`. |
| `gesture_sensitivity`| `float` | `0.7` | Confidence threshold for gesture detection (0.0 - 1.0). |
| `voice_sensitivity` | `float` | `0.6` | Confidence threshold for voice detection (0.0 - 1.0). |
| `debounce_time` | `float` | `0.5` | Minimum delay between commands in seconds. |
| `camera_index` | `integer`| `0` | Webcam index (0 for default, 1 for external). |
| `show_ui` | `boolean`| `true` | Display the real-time camera overlay and status. |
| `sound_effects` | `boolean`| `true` | Play audio feedback when a command is recognized. |
| `offline_mode` | `boolean`| `false` | Use local Vosk model for voice recognition instead of Google. |
| `language` | `string` | `"both"` | Active language: `"english"`, `"indonesian"`, or `"both"`. |

## API Reference

The project exposes a configuration manager that can be used programmatically:

```python
from config import config_manager, OperationMode

# Get a value
mode = config_manager.get_mode()

# Set a value (automatically saves to user_config.json)
config_manager.set_mode(OperationMode.GESTURE_ONLY)
config_manager.set("debounce_time", 1.0)
```

For more details on internal modules (`gesture_detector`, `voice_recognizer`, `controller`), refer to the source code docstrings.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT © [rab781](https://github.com/rab781)
