# Tutorial: Run Your First Presentation in 5 Minutes

**What you'll build**: You will configure and run the Presentation Control Tool to navigate a presentation completely hands-free.

**What you'll learn**:
- How to calibrate the tool for your environment
- How to use basic hand gestures and voice commands to control slides

**Prerequisites**:
- [ ] Python 3.8+ installed
- [ ] A working webcam and microphone
- [ ] A presentation software (e.g., PowerPoint, Google Slides, Canva)

---

## Step 1: Set Up Your Project

First, clone the repository and set up a virtual environment to isolate your dependencies.

```bash
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## Step 2: Install Dependencies

Install the required Python packages from `requirements.txt`.

```bash
pip install -r requirements.txt
```

> **Tip**: On Windows, if `pyaudio` fails to install, use the pre-compiled binary: `pip install pipwin && pipwin install pyaudio`.

## Step 3: Run the Calibration Wizard

Before presenting, you verify your setup and optimize detection settings using the built-in calibration wizard.

```bash
python main.py --calibrate
```

Follow the on-screen prompts to confirm your webcam framing, test your hand gestures, and measure your microphone input volume.

## Step 4: Start the Controller

Once calibrated, start the main controller application.

```bash
python main.py
```

A live preview of your webcam appears with an overlay indicating the current mode and detected gestures.

## Step 5: Control Your Presentation

Open your presentation software (like Google Slides) in the foreground and start the slideshow.

1. Stand 0.5 to 2 meters away from your webcam.
2. Ensure you are well-lit and your hand is fully visible.
3. **Swipe Right** with your hand (or say "next") to advance to the next slide.
4. **Swipe Left** with your hand (or say "previous") to return to the prior slide.

## Next Steps

You built a working hands-free presentation system. Here's what you learned:
- **Environment Setup**: How to initialize the tool.
- **Calibration**: Optimizing sensitivity settings.
- **Hybrid Control**: Combining gestures and voice commands.

- [Reference: Full Commands List](../reference/commands.md)
- [How-To: Set Up Offline Voice Recognition](../how-to/setup-offline-voice.md)
