# Presentation Control Tool

> Control your presentations hands-free using hand gestures and voice commands.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Exists

Clickers get lost, batteries die, and holding a device limits your expressiveness during a presentation. The Presentation Control Tool turns your webcam and microphone into a universal controller, automatically detecting your presentation software and letting you navigate slides fluidly without breaking your flow.

## Quick Start

```bash
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools
pip install -r requirements.txt
python main.py
```

Stand 0.5 to 2 meters from your webcam, open your presentation, and:
- **Swipe right** to go to the next slide.
- **Say "previous"** to go back.

## Installation

**Prerequisites**: Python 3.8+ and a working webcam and microphone.

First, set up a virtual environment to isolate your dependencies.

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Next, install the required packages. If you use macOS or Linux and see an error about `pywin32`, ignore it. It is a Windows-only package.

```bash
pip install -r requirements.txt
```

> **Tip**: If `pip install pyaudio` fails on Windows, install the pre-compiled binary instead:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

## Usage

### Basic Example

Start the controller by running the main script. Open your presentation (like PowerPoint or Google Slides), and use gestures or voice to navigate.

```bash
python main.py
```

### Configuration

Customize the application behavior by creating or editing `user_config.json` in the project root.

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

### Advanced Usage

For more details on interacting with the application, consult the documentation:

- [Configure Offline Voice Recognition](docs/how-to/configure-offline-voice.md)
- [Gestures and Voice Commands Reference](docs/reference/gestures-and-voice-commands.md)
- [Keyboard Controls Reference](docs/reference/keyboard-controls.md)

## API Reference

The project exposes a configuration manager that you use programmatically.

See the [API Reference →](docs/reference/api.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT © [Presentation Control Tool](https://github.com/rab781/Presentation-Tools)
