# Tutorial: Hands-Free Presentation Control in 15 Minutes

**What you'll build**: A local setup of the Presentation Control Tool that allows you to control a presentation (like PowerPoint or Google Slides) using hand gestures and voice commands.

**What you'll learn**:
- How to install the Presentation Control Tool and its dependencies
- How to calibrate your camera and microphone for optimal performance
- How to navigate slides using basic gestures and voice commands

**Prerequisites**:
- [ ] Python 3.8+ installed
- [ ] A working webcam and microphone
- [ ] A presentation application (e.g., PowerPoint, Google Slides, Canva)

---

## Step 1: Set Up Your Project

First, clone the repository and navigate into the project directory. We clone the repository so you have the latest source code and default configuration files ready to go.

```bash
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools
```

Next, create a virtual environment to isolate the project's dependencies from your system Python installation.

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## Step 2: Install Dependencies

Now, install the required packages using `pip`. This ensures you have OpenCV for gesture detection and SpeechRecognition for voice commands.

```bash
pip install -r requirements.txt
```

> **Tip**: If you use Windows and `pip install pyaudio` fails, install the pre-compiled binary instead by running `pip install pipwin` followed by `pipwin install pyaudio`. If you use macOS or Linux and see an error about `pywin32`, ignore it, as it is a Windows-only package.

## Step 3: Calibrate Your Setup

Before presenting, run the calibration wizard. The wizard tests your webcam and microphone, ensuring the tool can see your gestures and hear your voice clearly in your current environment.

```bash
python main.py --calibrate
```

Follow the on-screen prompts to test your camera and microphone. The wizard will recommend settings based on your lighting and background noise.

## Step 4: Control Your First Presentation

With everything installed and calibrated, start the main application.

```bash
python main.py
```

1. Open a presentation in PowerPoint or Google Slides.
2. Stand 0.5 to 2 meters from your webcam.
3. Swipe right with your hand to go to the next slide.
4. Say "previous" to go back to the previous slide.

You should see a small UI overlay on your camera feed showing the active mode and any detected commands.

## Step 5: What You Built

You successfully set up the Presentation Control Tool! Here's what you learned:
- **Project Setup**: How to clone the repository and isolate dependencies in a virtual environment.
- **Calibration**: How to use the built-in wizard to optimize detection for your environment.
- **Basic Usage**: How to run the tool and use gestures or voice to control slides.

## Next Steps

- [How-to: Offline Voice Recognition](../how-to/offline-voice.md)
- [Reference: API and Configuration](../reference/api-and-configuration.md)
- [Explanation: Architecture](../explanation/architecture.md)
