# Explanation: Architecture

This document explains the internal architecture of the Presentation Control Tool. It details how the main components interact to provide seamless, hands-free control of your presentations.

## High-Level Overview

The application is built around a central main loop (`main.py`) that coordinates three primary subsystems:
1. **Gesture Detection** (`gesture_detector.py`): Processes webcam frames to identify hand movements.
2. **Voice Recognition** (`voice_recognizer.py`): Listens for and transcribes spoken commands.
3. **Presentation Controller** (`controller.py`): Translates detected commands into simulated keystrokes for specific applications.

These systems run concurrently, governed by user configuration managed by the `ConfigManager` (`config.py`).

## The Main Loop

The `main.py` script acts as the orchestrator. When launched, it initializes the configured subsystems based on the chosen `mode` (gesture, voice, or hybrid).

The main loop continuously performs the following tasks:
- **Frame Capture**: Pulls the latest frame from the webcam (if gesture detection is active).
- **Processing**: Passes the frame to the `GestureDetector`.
- **UI Rendering**: Draws bounding boxes, status text, and the active mode onto the frame using OpenCV, then displays it.
- **Event Polling**: Checks for keyboard inputs (e.g., mode switching, pausing) via `cv2.waitKey`.

## Subsystem Interactions

### 1. Gesture Detection (OpenCV)

The `GestureDetector` relies on OpenCV for computer vision tasks.
- It maintains a background subtraction model to isolate moving objects (hands).
- It calculates the center of mass for detected contours to track hand position across frames.
- By comparing the current position to previous positions, it identifies directional swipes (left/right) or static shapes (open palm, closed fist).

When a gesture crosses the confidence threshold, the detector returns a standardized command string (e.g., `"next"` or `"previous"`).

### 2. Voice Recognition (SpeechRecognition & Vosk)

The `VoiceRecognizer` runs in a separate background thread to prevent audio processing from blocking the main webcam rendering loop.
- It uses the `SpeechRecognition` library to capture audio via PyAudio.
- By default, it sends audio chunks to the Google Web Speech API for transcription.
- If `offline_mode` is enabled, it bypasses Google and processes the audio locally using a Vosk model.

When transcription completes, the text is mapped against a dictionary of known commands (defined in `config.py`). If a match is found, the recognizer executes a callback provided by `main.py`, delivering the command string.

### 3. Presentation Controller (PyAutoGUI & PyGetWindow)

The `PresentationController` acts as the execution layer. It receives standardized commands from either the gesture or voice subsystem.
- **Application Detection**: It uses `pygetwindow` and `psutil` to identify the currently active foreground window (e.g., checking if PowerPoint or Chrome/Google Slides is in focus).
- **Command Translation**: It looks up the active application in the `APP_PROFILES` dictionary. This dictionary maps the standardized command (e.g., `"next"`) to the application-specific keyboard shortcut (e.g., `["right"]` for PowerPoint, or `["space"]` for Google Slides).
- **Execution**: It uses `pyautogui` to simulate the required keypresses, advancing the presentation. It also implements a debounce mechanism to prevent a single gesture from triggering multiple rapid commands.

## Configuration State

The `ConfigManager` is implemented as a singleton. Any component can import `config_manager` to read or update the current state. When a value is updated, the manager automatically serializes the new state to `user_config.json`, ensuring preferences persist across sessions.
