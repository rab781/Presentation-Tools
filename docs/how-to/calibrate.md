# How to Calibrate Your Setup

This guide explains how to run the built-in calibration wizard to diagnose and fix hardware or environmental issues preventing the Presentation Control Tool from working correctly.

The calibration wizard automatically tests your webcam, microphone, keyboard control, and application detection.

## Step 1: Run the Calibration Wizard on Startup

If you are experiencing issues immediately, run the calibration wizard on startup by passing the `--calibrate` (or `-c`) flag to the main script.

```bash
python main.py --calibrate
```

## Step 2: Run the Calibration Wizard While Running

If the application is already running and you want to test the current setup without restarting, press `C` on your keyboard while the application window is active.

## Step 3: Interpret the Results

The wizard will test the following components sequentially:

1.  **Camera**: Checks if the camera can be opened and frames can be captured.
2.  **Microphone**: Checks if the microphone is working and adjusts the energy threshold for ambient noise.
3.  **Keyboard**: Checks if the `pyautogui` library can simulate key presses.
4.  **Application Detection**: Detects the currently active application profile (e.g., PowerPoint, Google Slides).

Read the output in the console to identify any failing tests (marked with `✗`). Successful tests are marked with `✓`.

## Troubleshooting

Based on the test results, follow these steps to resolve common issues:

-   **Camera Error**: If the camera fails to open, ensure no other application is using it. You may need to change the `camera_index` in your configuration if you have multiple cameras.
-   **Microphone Error**: Ensure your microphone is properly connected and selected as the default recording device in your operating system settings.
-   **Poor Gesture Detection**: Ensure good lighting on your hands and position the camera 0.5 to 2 meters away.
-   **Poor Voice Recognition**: Reduce background noise. If you are using offline mode, ensure the Vosk model is installed correctly.
