# Presentation Control Tool

> A universal presentation controller that turns your webcam and microphone into a hands-free presentation clicker using computer vision and voice recognition.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Exists

Presenting shouldn't tie you to a keyboard or a physical clicker. Physical clickers get lost, their batteries die unexpectedly, and holding a device limits your physical expressiveness. The Presentation Control Tool solves this by allowing you to navigate slides naturally using simple hand gestures or voice commands, keeping your hands free to present.

## Quick Start

Get the controller running locally in under 3 minutes.

```bash
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools
pip install -r requirements.txt
python main.py
```

Stand back from your camera, open any presentation software, and **swipe right** in the air or say **"next"** to advance your slides.

## Installation

**Prerequisites**:
- Python 3.8+
- A working webcam
- A working microphone

We recommend setting up a virtual environment to isolate the project dependencies.

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the required packages.

```bash
pip install -r requirements.txt
```

> **Note for macOS/Linux Users**: If you see an error about `pywin32` during installation, you can safely ignore it. This package is Windows-specific for active application detection.

> **Note for Windows Users**: If `pip install pyaudio` fails, install the pre-compiled binary instead:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

## Usage

### Basic Example

To start controlling your presentations, run the main script. The tool automatically detects your active application (PowerPoint, Google Slides, Canva, PDF Viewer) and maps the appropriate keyboard shortcuts.

```bash
python main.py
```

Stand 0.5 to 2 meters from your webcam. You can now use gestures or voice to navigate.

**Most common commands:**
- **Swipe right** in front of the camera: Next slide.
- **Swipe left** in front of the camera: Previous slide.
- Say **"next"**: Next slide.

If you encounter accuracy issues with gestures or voice recognition, run the calibration wizard:

```bash
python main.py --calibrate
```

### Configuration

You customize the application behavior by creating or editing a `user_config.json` file in the project root directory.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | `string` | `"hybrid"` | Operation mode: `"gesture"`, `"voice"`, or `"hybrid"`. |
| `gesture_sensitivity`| `float` | `0.7` | Confidence threshold for gesture detection (0.0 - 1.0). |
| `voice_sensitivity` | `float` | `0.6` | Confidence threshold for voice detection (0.0 - 1.0). |
| `debounce_time` | `float` | `0.5` | Minimum delay between commands in seconds to prevent double triggers. |
| `camera_index` | `integer`| `0` | Webcam index (0 for default, 1 for external). |
| `show_ui` | `boolean`| `true` | Display the real-time camera overlay and status. |
| `sound_effects` | `boolean`| `true` | Play audio feedback when you successfully issue a command. |
| `offline_mode` | `boolean`| `false` | Use local Vosk model for voice recognition instead of Google. |
| `language` | `string` | `"both"` | Active language for voice recognition: `"english"`, `"indonesian"`, or `"both"`. |

### Advanced Usage

#### Supported Hand Gestures

| Gesture | Command | Action |
|---------|---------|--------|
| 👉 Swipe Right | Next | Next slide |
| 👈 Swipe Left | Previous | Previous slide |
| ✋ Open Palm | Pause | Pause/Blackout |
| ✊ Closed Fist | Play | Resume |
| 👍 Thumbs Up | First | First slide |
| 👎 Thumbs Down | Last | Last slide |
| ✌️ Peace Sign | Blackout | Black screen |

#### Supported Voice Commands

You can use English or Indonesian commands out of the box.

- **Navigation**: "next", "previous", "back", "first", "last", "start", "end"
- **Control**: "pause", "stop", "play", "resume", "exit", "quit"
- **Indonesian**: "lanjut", "berikutnya", "kembali", "sebelumnya", "pertama", "terakhir", "berhenti", "jeda", "lanjutkan", "mulai", "keluar"

#### Enabling Offline Voice Recognition

By default, the tool uses Google's Speech Recognition API. To work completely offline with zero latency, you configure a local Vosk model.

1. Create a `models` directory in the project root: `mkdir models`.
2. Download the [Vosk Indonesian Small Model](https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip) (or an English equivalent).
3. Extract the contents directly into the `models/vosk-model-small-id-0.22` directory.
4. Set `"offline_mode": true` in your `user_config.json`.

#### In-App Keyboard Controls

While the application is actively running, you press these keys on the active UI window to control the tool's behavior:

| Key | Function |
|-----|----------|
| **G** | Switch to Gesture Only mode |
| **V** | Switch to Voice Only mode |
| **H** | Switch to Hybrid mode (both gesture and voice enabled) |
| **C** | Run calibration wizard |
| **A** | Auto-detect active presentation application manually |
| **P** | Pause/Resume all detection |
| **ESC** | Exit application gracefully |

## API Reference

The project exposes a configuration manager that you import to manage the presentation controller programmatically in your own scripts.

```python
from config import config_manager, OperationMode

# Retrieve the current mode
mode = config_manager.get_mode()

# Set a value (this automatically saves to user_config.json)
config_manager.set_mode(OperationMode.GESTURE_ONLY)
config_manager.set("debounce_time", 1.0)
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to help improve the project.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT © [Presentation Control Tool](https://github.com/rab781/Presentation-Tools)
