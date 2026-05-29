# Tutorial: Control Your First Presentation in 15 Minutes

**What you'll build**: You will set up the Presentation Control Tool and use your hand gestures to navigate through a slide presentation.

**What you'll learn**:
- How to install the Presentation Control Tool and its dependencies
- How to start the tool in Gesture Only mode
- How to perform basic swipe gestures to control slides

**Prerequisites**:
- [ ] Python 3.8+ installed
- [ ] A working webcam
- [ ] A presentation application (like PowerPoint or Google Slides)

---

## Step 1: Set Up Your Project

First, clone the repository and navigate into the project directory.

```bash
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools
```

Next, create a virtual environment. We use a virtual environment to isolate the project's dependencies from your system Python.

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> **Tip**: If you see permission errors on Windows when activating the environment, run your terminal as an Administrator or use `Set-ExecutionPolicy Unrestricted -Scope CurrentUser`.

## Step 2: Install Dependencies

Now, install the required packages.

```bash
pip install -r requirements.txt
```

> **Tip**: If you use macOS or Linux and see an error about `pywin32`, ignore it. It is a Windows-only package.
> On Windows, if `pip install pyaudio` fails, run `pip install pipwin` followed by `pipwin install pyaudio`.

## Step 3: Open Your Presentation

Open a slide deck in your preferred presentation software. The tool automatically detects common applications:
- Microsoft PowerPoint
- Google Slides (in a browser)
- PDF Viewers
- Canva

Make sure your presentation is in full-screen or "Present" mode.

## Step 4: Run the Tool

Start the main application.

```bash
python main.py
```

A camera preview window will appear on your screen showing your webcam feed.

## Step 5: Control Your Slides

Stand or sit about 0.5 to 2 meters away from your webcam. Make sure your hand is clearly visible in the camera frame.

1. **Go to the next slide**: Hold your hand up and swipe it quickly to the right. You should see a green circle track your hand, and the slide will advance.
2. **Go to the previous slide**: Swipe your hand quickly to the left. The slide will go back.

> **Tip**: If the application doesn't seem to recognize your presentation software, select its window to bring it to the foreground, then press `A` on your keyboard while the camera window is active to auto-detect the application.

## Step 6: What You Built

You successfully set up the Presentation Control Tool and controlled your slides hands-free! Here's what you learned:
- **Installation**: How to set up a Python virtual environment and install dependencies.
- **Gesture Control**: How to use swipe gestures to navigate slides.

## Next Steps

- [How-To Guide: Configure Offline Voice Recognition](how-to-guides.md#configure-offline-voice-recognition)
- [How-To Guide: Run the Calibration Wizard](how-to-guides.md#run-the-calibration-wizard)
- [Reference: Full Gesture and Voice Commands](reference.md)
