# Tutorial: Control Your First Presentation in 15 Minutes

**What you'll build**: A working local installation of the Presentation Control Tool that lets you change slides using hand gestures and voice commands.

**What you'll learn**:
- How to install the Presentation Control Tool
- How to start the application in hybrid mode
- How to perform basic swipe gestures and voice commands to control a presentation

**Prerequisites**:
- [ ] Python 3.8+ installed
- [ ] A working webcam
- [ ] A working microphone
- [ ] Any presentation software (e.g., PowerPoint, Google Slides)

---

## Step 1: Set Up Your Project

First, create a new directory for your project and clone the repository. We use a separate virtual environment to keep things clean and avoid dependency conflicts.

```bash
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools
```

Create and activate the virtual environment:

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> **Tip**: If you see permissions errors activating the script on Windows, run `Set-ExecutionPolicy Unrestricted -Scope CurrentUser` in PowerShell first.

## Step 2: Install Dependencies

Next, install the required packages.

```bash
pip install -r requirements.txt
```

> **Tip**: If you are using macOS or Linux, you might see an error regarding `pywin32`. You can safely ignore this, as `pywin32` is a Windows-only package used for auto-detecting the active presentation window. The tool falls back to a "universal" profile automatically.
> If `pip install pyaudio` fails on Windows, install the pre-compiled binary instead:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

## Step 3: Run the Application

Start the controller by running the main script.

```bash
python main.py
```

You should see output indicating that gesture detection and voice recognition are initialized, and a UI window should appear showing your webcam feed.

The application starts in **Hybrid Mode** by default, meaning both gestures and voice commands are active.

## Step 4: Control Your Presentation

Open your presentation software (like PowerPoint or Google Slides) and start presenting.

Ensure you are standing 0.5 to 2 meters from your webcam.

Try these commands to navigate:
- **Gesture**: Swipe your hand right to go to the next slide.
- **Gesture**: Swipe your hand left to go to the previous slide.
- **Voice**: Say "next" to go to the next slide.
- **Voice**: Say "previous" to go to the previous slide.

The controller automatically detects your active application and maps these actions to the appropriate keyboard shortcuts (e.g., `Right Arrow` for next slide, `Left Arrow` for previous slide).

## Step 5: What You Built

You successfully installed and ran the Presentation Control Tool! Here's what you learned:
- **Project Setup**: How to clone the repository and install dependencies in an isolated environment.
- **Execution**: How to start the application and verify it is running correctly.
- **Control**: How to use basic gestures and voice commands to navigate slides.

## Next Steps

- [How-to Guide: Calibrate Your Setup](../how-to/calibrate.md)
- [How-to Guide: Configure Offline Voice Recognition](../how-to/offline_voice.md)
- [Reference: API and Configuration](../reference/api.md)
