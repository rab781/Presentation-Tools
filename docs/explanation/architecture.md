# Explanation: Architecture

This document explains the high-level architecture of the Presentation Control application, detailing how the distinct modules communicate to map physical movements into software actions.

## The Core Loop (`main.py`)

The application is orchestrated by `PresentationToolApp` inside `main.py`. It runs a continuous `while` loop that acts as the central router for data.

At a high level, the loop performs three tasks every frame:
1. Polls the camera and passes the frame to the `GestureDetector`.
2. Checks for keyboard events (like mode switching).
3. Updates the graphical user interface.

## Module Communication

The system is decoupled into three primary engines, allowing them to operate independently based on the user's selected mode (Gesture, Voice, or Hybrid).

### 1. `GestureDetector` (Vision)
When the main loop calls `detect_gesture()`, the detector uses OpenCV to evaluate the frame for motion differences.
If a gesture meets the required confidence threshold, it returns a string identifier (e.g., `"SWIPE_RIGHT"`). The main loop then routes this identifier to the `PresentationController`.

### 2. `VoiceRecognizer` (Audio)
Unlike the gesture system which is polled synchronously, the `VoiceRecognizer` runs in a background thread to prevent audio processing from blocking the camera feed.

It continuously listens to the microphone. When a spoken phrase is recognized (via Google Speech or local Vosk model), it executes a callback function `_on_voice_command` defined in the main application. This callback pushes the resulting command string directly to the `PresentationController`.

### 3. `PresentationController` (Execution)
The controller acts as the translation layer between the tool and the operating system. When it receives a command string (like `"next"`) from either the gesture or voice systems, it determines the active application profile (e.g., PowerPoint vs Google Slides) using `win32gui` and `psutil`.

It looks up the appropriate keyboard shortcut for that application in the `APP_PROFILES` dictionary and uses `pyautogui` to simulate the physical key press.

## UI Optimization

To maintain high framerates while rendering real-time text and bounding boxes over the camera feed, the UI rendering in `main.py` is heavily optimized.

Instead of copying and blending the entire frame to create the semi-transparent status bar, the application uses **Region of Interest (ROI) blending**. It slices only the top 120 pixels of the image array and performs an in-place alpha blend using `cv2.addWeighted`. This prevents expensive memory allocation and reduces computational overhead by approximately 75% per frame.