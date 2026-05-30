# System Architecture

This document explains the high-level architecture of the Presentation Control Tool, detailing how the different components interact to enable hands-free presentation control.

## Overview

The system is composed of three primary modules, orchestrated by a central main application loop.

1.  **`GestureDetector`**: Captures video frames from the webcam and processes them using OpenCV and MediaPipe to identify hand gestures.
2.  **`VoiceRecognizer`**: Captures audio from the microphone and processes it using either Google Speech Recognition (online) or Vosk (offline) to identify voice commands.
3.  **`PresentationController`**: Receives commands from the gesture and voice modules, translates them into application-specific keyboard shortcuts, and executes them using PyAutoGUI.

## Component Interaction

The `PresentationToolApp` in `main.py` serves as the central orchestrator.

### The Input Loop

The application runs a continuous loop (`while self.running`). During each iteration:

1.  **Gesture Processing**: The app queries the `GestureDetector` for a new frame. If a hand is detected, the detector maps the gesture to a command (e.g., "SWIPE_RIGHT" -> "next") and returns it.
2.  **Voice Processing**: The `VoiceRecognizer` runs in a separate background thread, continuously listening for audio. When a command is recognized, it places the command in a thread-safe queue. The main application app registers a callback (`_on_voice_command`) that handles these commands.
3.  **Command Routing**: Commands from either source are passed to the `PresentationController` via `controller.send_command()`.

### The Controller Queue

The `PresentationController` also runs in its own background thread. This design ensures that executing slow keyboard simulations (or blocking system calls to detect the active window) does not freeze the real-time webcam feed or audio listening.

1.  **Debouncing**: When a command is received, the controller checks the time elapsed since the last identical command. If it's less than the configured `debounce_time`, the command is ignored. This prevents accidental double-swipes.
2.  **Application Detection**: The controller uses `win32gui` and `psutil` (on Windows) to determine which application is currently in the foreground. It caches this information for performance.
3.  **Execution**: The controller maps the generic command (e.g., "next") to the specific keyboard shortcut for the active application (e.g., `Right Arrow` for PowerPoint, `Space` for Google Slides) and uses `pyautogui.press()` to execute it.

## Concurrency

The system utilizes threading to maintain a responsive UI and accurate detection:

-   **Main Thread**: Handles the webcam frame capture loop, UI rendering (`cv2.imshow`), and keyboard input for mode switching.
-   **Voice Thread**: Handles audio stream listening and processing.
-   **Controller Thread**: Handles command queue processing and keyboard simulation.

This separation prevents expensive operations (like network requests for voice recognition or complex OpenCV calculations) from blocking each other.