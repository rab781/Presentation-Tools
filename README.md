# Presentation Control Tool

> Control your presentations hands-free using hand gestures and voice commands.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10%2B-orange)](https://developers.google.com/mediapipe)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Exists

Presenters are often tied to their keyboards, clickers, or podiums, interrupting their flow to change slides. The Presentation Control Tool eliminates this friction by allowing you to navigate slides, pause presentations, and jump to sections using intuitive hand gestures or voice commands, enabling a more natural and engaging presentation style.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools

# Install requirements
pip install -r requirements.txt

# Run the tool
python main.py
```

You should see the application window open and initialize your camera and microphone. Make a "Thumbs Up" gesture to jump to the first slide!

## Installation

**Prerequisites**: Python 3.8+, a webcam, and a microphone.

```bash
# Optional but recommended: Create a virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Windows PyAudio Troubleshooting

If you encounter errors installing `PyAudio` on Windows, it is likely due to missing build tools. Use one of these alternatives:

**Option 1: Use pipwin (Recommended)**
```powershell
pip install pipwin
pipwin install pyaudio
```

**Option 2: Pre-built Wheels**
Download the correct `.whl` file from [Unofficial Windows Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) matching your Python version, then run `pip install <filename>.whl`.

### Offline Voice Recognition (Optional)

If you plan to use voice commands without an internet connection, download a Vosk model (e.g., Indonesian or English):

```bash
mkdir models
cd models
# Example: Download the small Indonesian model (~50MB)
Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip" -OutFile "vosk-model-small-id-0.22.zip"
Expand-Archive -Path "vosk-model-small-id-0.22.zip" -DestinationPath "."
cd ..
```

## Usage

### Basic Example

Start the application with default settings:

```bash
python main.py
```

When running, the tool auto-detects your active presentation software (PowerPoint, Google Slides, PDF Viewers, Canva). Use the following controls:

| Gesture | Voice Command (EN/ID) | Action |
|---------|-----------------------|--------|
| 👉 Swipe Right | "Next" / "Lanjut" | Next slide |
| 👈 Swipe Left | "Previous" / "Kembali" | Previous slide |
| ✋ Open Palm | "Pause" / "Jeda" | Pause/Blackout |
| ✊ Closed Fist | "Play" / "Mulai" | Resume |
| 👍 Thumbs Up | "First" / "Pertama" | First slide |
| 👎 Thumbs Down| "Last" / "Terakhir" | Last slide |
| ✌️ Peace Sign | "Blackout" / "Hitam" | Black screen |

**In-App Hotkeys**:
*   `G`: Gesture Only mode
*   `V`: Voice Only mode
*   `H`: Hybrid mode (Both)
*   `C`: Run calibration wizard
*   `A`: Auto-detect active application
*   `P`: Pause/Resume detection
*   `ESC`: Exit

### Configuration

You can customize the tool's behavior by editing `config.py` or creating a `user_config.json` file in the project root:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | `string` | `"hybrid"` | Operation mode: `"gesture"`, `"voice"`, or `"hybrid"`. |
| `gesture_sensitivity` | `float` | `0.7` | Confidence threshold for hand tracking (0.0 to 1.0). |
| `voice_sensitivity` | `float` | `0.6` | Confidence threshold for voice commands. |
| `debounce_time` | `float` | `0.5` | Delay (in seconds) between commands to prevent rapid firing. |
| `camera_index` | `integer`| `0` | System camera index (`0` for default, `1` for external). |
| `show_ui` | `boolean`| `true` | Display the visual overlay with status and FPS. |
| `sound_effects` | `boolean`| `true` | Play audio feedback (beeps) when a command is executed. |
| `offline_mode` | `boolean`| `false` | Force the use of Vosk for offline voice recognition. |
| `language` | `string` | `"both"` | Voice command language: `"indonesian"`, `"english"`, or `"both"`. |

**Example `user_config.json`**:
```json
{
  "mode": "gesture",
  "gesture_sensitivity": 0.8,
  "show_ui": false,
  "sound_effects": false
}
```

### Advanced Usage

**Calibration Wizard**
If the tool struggles to detect your gestures or voice, run the built-in calibration wizard before your presentation. It tests your camera, microphone, and application detection to recommend the best setup.

```bash
python main.py --calibrate
```

## Supported Applications

The tool simulates keyboard shortcuts tailored to specific applications. If an app isn't explicitly supported, it falls back to a "Universal" profile (standard arrow keys).

| Application | Auto-detect | Status |
|-------------|-------------|--------|
| PowerPoint | ✅ Yes | Fully supported |
| Google Slides | ✅ Yes | Fully supported |
| PDF Viewers | ✅ Yes | Supported |
| Canva | ✅ Yes | Limited support |
| Universal | - | Fallback mode |

## Contributing

We welcome pull requests! If you're adding support for a new presentation app or a custom gesture, please refer to our codebase structure:
*   `gesture_detector.py`: Hand tracking logic (MediaPipe).
*   `voice_recognizer.py`: Speech recognition logic.
*   `controller.py`: Keyboard simulation (PyAutoGUI/win32).
*   `config.py`: Default settings and command mappings.

## License

MIT © [rab781](https://github.com/rab781)
