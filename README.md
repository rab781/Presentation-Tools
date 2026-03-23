# Presentation Control Tool

> Control your presentations hands-free using computer vision and voice commands.

[![Python version](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Exists

Being tied to a keyboard or carrying a clicker interrupts the flow of a good presentation. You need a way to navigate slides naturally while speaking and moving around the stage. This tool uses your webcam and microphone to let you control PowerPoint, Google Slides, and other presentation software using intuitive hand gestures and voice commands.

## Quick Start

The fastest way to get started is by cloning the repository and running the application:

```bash
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1
# Linux/macOS
# source venv/bin/activate

pip install -r requirements.txt
python main.py
```

## Installation

**Prerequisites**: Python 3.8+ and a working webcam/microphone. Windows 10/11 is recommended.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rab781/Presentation-Tools.git
   cd Presentation-Tools
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   > **Note on PyAudio (Windows):** If you encounter errors installing PyAudio, install it using a pre-built wheel from [Unofficial Windows Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) matching your Python version, or use `pipwin`:
   > ```bash
   > pip install pipwin
   > pipwin install pyaudio
   > ```

4. **(Optional) Offline Voice Recognition:**
   If you want to use voice commands without an internet connection, download the Vosk model for your language (e.g., [Indonesian Small Model](https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip)) and extract it into a `models/` directory in the project root. Update `config.py` to enable offline mode.

## Usage

Start the main application to begin controlling your presentation:

```bash
python main.py
```

### Basic Modes

The tool supports three operational modes. You switch between them while the application is running using these hotkeys:

- **G**: **Gesture Only** - Navigate using only hand movements.
- **V**: **Voice Only** - Navigate using spoken commands.
- **H**: **Hybrid** - Navigate using both gestures and voice.
- **P**: **Pause/Resume** - Temporarily stop detection.
- **C**: **Calibrate** - Run the setup wizard to test your camera and microphone.
- **A**: **Auto-detect** - Force the application to detect the currently active presentation software.
- **ESC**: **Exit** - Close the application.

### Hand Gestures

Ensure you are 0.5 to 2 meters away from the camera in a well-lit room.

| Action | Gesture | Description |
|---|---|---|
| **Next Slide** | 👉 Swipe Right | Quick horizontal movement to the right |
| **Previous Slide** | 👈 Swipe Left | Quick horizontal movement to the left |
| **Pause/Blackout** | ✋ Open Palm | Hold hand open |
| **Resume** | ✊ Closed Fist | Clench hand into a fist |
| **First Slide** | 👍 Thumbs Up | Thumb pointing upwards |
| **Last Slide** | 👎 Thumbs Down | Thumb pointing downwards |

### Voice Commands

The tool supports both Indonesian and English commands. Speak clearly towards your microphone.

| Action | English Commands | Indonesian Commands |
|---|---|---|
| **Next Slide** | "next", "forward" | "lanjut", "berikutnya", "selanjutnya" |
| **Previous Slide** | "previous", "back" | "kembali", "sebelumnya", "mundur" |
| **First Slide** | "first", "start" | "pertama", "awal", "mulai" |
| **Last Slide** | "last", "end" | "terakhir", "akhir" |
| **Pause** | "pause", "stop" | "berhenti", "jeda" |
| **Resume** | "play", "resume" | "lanjutkan", "mulai" |
| **Exit** | "exit", "quit", "close" | "keluar", "tutup" |

### Configuration

You customize the tool's behavior by editing the generated `user_config.json` file or the default `config.py`.

| Option | Type | Default | Description |
|---|---|---|---|
| `mode` | `string` | `"hybrid"` | Initial mode: `"gesture"`, `"voice"`, or `"hybrid"`. |
| `gesture_sensitivity` | `float` | `0.7` | Sensitivity threshold for hand tracking (0.0 to 1.0). |
| `voice_sensitivity` | `float` | `0.6` | Confidence threshold for voice recognition. |
| `debounce_time` | `float` | `0.5` | Delay (in seconds) between accepting consecutive commands. |
| `camera_index` | `int` | `0` | Camera device index (0 for default webcam, 1 for external). |
| `show_ui` | `boolean` | `true` | Show the camera feed and overlay status. |
| `sound_effects` | `boolean` | `true` | Play an audio beep when a command is recognized. |

## Supported Applications

The tool automatically detects the active application and uses the correct keyboard shortcuts.

- **PowerPoint**: Fully supported (Navigation, Start, Blackout)
- **Google Slides**: Fully supported (Navigation, Speaker Notes)
- **PDF Viewers** (Acrobat, Foxit): Navigation supported
- **Canva**: Navigation supported
- **Universal Mode**: Uses standard arrow keys as a fallback for unknown applications.

## Troubleshooting

- **Camera not detected**: Ensure no other application is using your webcam. Test it directly with OpenCV: `python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Error')"`.
- **Commands are triggering twice**: Increase the `debounce_time` in your configuration file.
- **Voice recognition is missing words**: Run the calibration wizard (`python main.py --calibrate`) to adjust your microphone's energy threshold based on your room's ambient noise.
- **Application shortcuts aren't working**: Ensure the presentation window (e.g., PowerPoint) has focus. Press 'A' to force the tool to re-detect the active application.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) (if available). We welcome pull requests for bug fixes and new features.

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

MIT © [rab781](https://github.com/rab781)
