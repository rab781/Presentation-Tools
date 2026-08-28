# Tutorial: Getting Started with Presentation Control Tool

**What you'll build**: A working local environment for the Presentation Control Tool that allows you to navigate presentations using hand gestures and voice commands.

**What you'll learn**:
- How to install the Presentation Control Tool
- How to start the application
- How to navigate a presentation

**Prerequisites**:
- [ ] Python 3.8+ installed
- [ ] A working webcam and microphone

---

## Step 1: Set Up Your Project

First, create a new directory for the project and initialize a virtual environment. This keeps the dependencies isolated from your system Python environment.

```bash
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools
```

Create and activate a virtual environment:

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## Step 2: Install Dependencies

Next, install the required packages.

```bash
pip install -r requirements.txt
```

> **Tip**: If you use macOS or Linux and see an error about `pywin32`, ignore it. It is a Windows-only package. If `pip install pyaudio` fails on Windows, install the pre-compiled binary instead:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

## Step 3: Run the System Check

Run the test script to verify that all required modules are imported correctly and that your camera and microphone are accessible.

```bash
python test_setup.py
```

If any tests fail, check the output for troubleshooting steps.

## Step 4: Start the Application

Start the controller by running the main script. Stand 0.5 to 2 meters from your webcam.

```bash
python main.py
```

Open a presentation in PowerPoint, Google Slides, or a PDF Viewer. Try swiping right to go to the next slide, or say "previous" to go back.

## What You Built

You built a working environment for the Presentation Control Tool. Here's what you learned:
- **Installation**: How to isolate dependencies and install the required packages.
- **Verification**: How to run the system check to ensure your hardware is ready.
- **Execution**: How to start the application and use basic gestures and voice commands.

## Next Steps

- [How-To: Calibrate Your Setup](../how-to/calibrate.md)
- [How-To: Configure Offline Voice](../how-to/configure-offline-voice.md)
- [Reference: Configuration Options](../reference/configuration.md)
