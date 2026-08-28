# Tutorial: Get Started with Presentation Control in 5 Minutes

**What you'll build**: A hands-free presentation setup allowing you to navigate slides with simple hand gestures and voice commands.

**What you'll learn**:
- Starting the Presentation Control tool
- Calibrating your setup for accurate gesture and voice detection
- Controlling your slides
- Switching between gesture, voice, and hybrid modes

**Prerequisites**:
- [ ] Presentation Control Tool installed (see [README.md](../../README.md) for installation instructions)
- [ ] A presentation application running (e.g., PowerPoint, Google Slides, Canva)
- [ ] A working webcam and microphone

---

## Step 1: Start the Application

First, open your terminal, navigate to the project directory, and run the main application script.

```bash
python main.py
```

You will see the application load, and a camera window named "Presentation Controller" will appear displaying your webcam feed.

## Step 2: Calibrate Your Setup

To ensure accurate gesture and voice detection, run the calibration wizard. The wizard tests your camera, microphone, and application detection.

Stop the current application using `ESC`, then run it with the calibrate flag:

```bash
python main.py --calibrate
```

Follow the on-screen prompts to verify your camera resolution, microphone energy threshold, and detected application.

## Step 3: Test Gestures and Voice

Start your presentation in PowerPoint, Google Slides, or Canva. Position yourself 0.5 to 2 meters from the camera.

Start the application again:

```bash
python main.py
```

Perform a **Swipe Right** gesture (moving your hand horizontally to the right across the camera view) or say **"Next"** to navigate to the next slide.

Perform a **Swipe Left** gesture or say **"Previous"** to go back.

## Step 4: Switch Operation Modes

By default, the application runs in Hybrid mode (both gesture and voice enabled). You can change this using keyboard shortcuts while the application window is active.

Press `g` to switch to **Gesture Only** mode.
Press `v` to switch to **Voice Only** mode.
Press `h` to switch back to **Hybrid** mode.

## What You Built

You built a fully configured environment to present without a clicker! Here's what you learned:
- **Starting & Calibrating**: How to initialize the tool and ensure optimal hardware performance.
- **Navigating**: How to trigger next and previous commands.
- **Mode Switching**: How to isolate gesture or voice controls depending on your environment.

## Next Steps

- [How-To: Configure Offline Voice Recognition](../how-to/offline_voice.md)
- [Reference: View all Gestures and Commands](../reference/commands.md)
- [Reference: Advanced Configuration](../reference/configuration.md)