# Tutorial: Control a Presentation Hands-Free in 5 Minutes

**What you'll build**: A working setup that lets you control a presentation (PowerPoint, Google Slides, etc.) using your webcam and microphone without touching a physical device.

**What you'll learn**:
- How to start the Presentation Control Tool
- How to navigate slides using hand gestures
- How to control your presentation using voice commands

**Prerequisites**:
- [ ] Python 3.8+ installed
- [ ] A working webcam and microphone
- [ ] Presentation software (PowerPoint, Google Slides, Canva, or a PDF viewer)
- [ ] The `Presentation-Tools` repository cloned and dependencies installed (see [README](../README.md#installation))

---

## Step 1: Start the Application

First, you run the main application script. This initializes the camera, microphone, and the controller logic that simulates keyboard presses.

```bash
python main.py
```

You should see output indicating that gesture detection and voice recognition are initialized, along with a window popping up showing your webcam feed.

> **Tip**: Ensure you are in a well-lit room and sitting 0.5 - 2 meters from your webcam for best gesture detection.

## Step 2: Open Your Presentation

Open any slide deck in PowerPoint, Google Slides, or a PDF viewer and start presenting (e.g., press `F5` in PowerPoint or "Slideshow" in Google Slides). The tool automatically detects the active presentation software and maps your commands to the correct keyboard shortcuts.

## Step 3: Navigate with Hand Gestures

With the camera feed visible (or running in the background), test the basic swipe gestures to move between slides.

1. Raise your hand so it is clearly visible in the camera frame.
2. **Swipe your hand right** to go to the next slide.
3. **Swipe your hand left** to go back to the previous slide.

You should see the slide change in your presentation, and the on-screen UI (if enabled) will display "Last: next (gesture)" or "Last: previous (gesture)".

## Step 4: Control with Voice Commands

Next, try using your voice. The application listens continuously and uses Google Speech Recognition (or a local Vosk model if configured) to detect commands.

1. Say clearly: **"Next"** (or **"Lanjut"** in Indonesian).
2. The slide will advance.
3. Say: **"Previous"** (or **"Kembali"**).
4. The slide will return to the previous one.

If you want to pause your presentation temporarily, you can also use commands like **"Pause"** or **"Blackout"**, and then **"Play"** or **"Resume"** to continue.

## What You Built

You successfully set up and used a hands-free presentation controller! Here's what you learned:
- **Starting the Tool**: How to initialize the `main.py` application.
- **Gesture Navigation**: How to use directional swipes to change slides.
- **Voice Navigation**: How to use spoken commands to control the presentation.

## Next Steps

- [How-To Guide: Change Operation Modes](how-to.md#change-operation-modes)
- [Reference: View All Supported Commands](reference.md#supported-interactions)
- [Explanation: Understand How the System Works](explanation.md)
