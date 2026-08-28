# Presentation Control Tool

> Control your presentations hands-free using hand gestures and voice commands.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Exists

Clickers get lost, batteries die, and holding a device limits your expressiveness during a presentation. The Presentation Control Tool solves this by turning your webcam and microphone into a universal controller, allowing you to navigate slides fluidly without breaking your flow.

## Quick Start

```bash
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools
pip install -r requirements.txt
python main.py
```

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

Start the controller by running the main script. Stand 0.5 to 2 meters from your webcam, open your presentation (like PowerPoint or Google Slides), and use gestures or voice to navigate.

```bash
python main.py
```

- **Swipe right** to go to the next slide.
- **Say "previous"** to go back.

### Configuration & Documentation

For full details on configuring the tool, using offline voice recognition, and advanced usage, refer to the documentation:

- [Tutorial: Getting Started](docs/tutorials/getting-started.md)
- [How-To: Configure Offline Voice](docs/how-to/configure-offline-voice.md)
- [How-To: Calibrate Your Setup](docs/how-to/calibrate.md)
- [Reference: Configuration Options](docs/reference/configuration.md)
- [Explanation: Architecture](docs/explanation/architecture.md)

## API Reference

See the [API Reference](docs/reference/api.md) for programmatic usage of the configuration manager.

## Contributing

Contributions are welcome! Please submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT © [Presentation Control Tool](https://github.com/rab781/Presentation-Tools)
