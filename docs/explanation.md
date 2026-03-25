# Architecture & Explanation

The Presentation Control Tool turns your webcam and microphone into a universal presentation remote. This document explains the design decisions and architectural components that make this possible.

## Why Build This?

Physical clickers are often misplaced, require batteries, and restrict your movement on stage. By leveraging the built-in webcam and microphone on modern laptops, you can navigate presentations using natural gestures and voice commands, allowing for a more expressive and engaging presentation style.

## System Architecture

The tool is built using a modular architecture with three core components:

1. **Gesture Detector (`gesture_detector.py`)**
2. **Voice Recognizer (`voice_recognizer.py`)**
3. **Presentation Controller (`controller.py`)**

These components run in separate threads and communicate via thread-safe queues. This ensures that expensive operations (like computer vision processing or network requests for speech recognition) do not block the main application loop or user interface.

### Gesture Detection

The gesture detector uses a simple computer vision approach (via OpenCV) rather than relying on complex machine learning models (like MediaPipe) for its initial implementation. This keeps the resource footprint low and makes the tool accessible on less powerful hardware.

**How it works:**
1. **Frame Capture**: Reads frames from the webcam.
2. **Preprocessing**: Converts the frame to grayscale and applies a Gaussian blur to reduce noise.
3. **Motion Detection**: Computes the absolute difference (`cv2.absdiff`) between the current frame and the previous frame to identify areas of motion.
4. **Contour Analysis**: Finds the largest moving contour (assumed to be the hand) and calculates its center of mass (`cv2.moments`).
5. **Swipe Recognition**: Tracks the center point across frames. If the horizontal displacement exceeds a threshold (`swipe_threshold`), it triggers a "Next" or "Previous" command.

### Voice Recognition

The voice recognizer provides hands-free control using a combination of online and offline speech-to-text engines.

**How it works:**
1. **Continuous Listening**: A background thread keeps the microphone stream open, listening for audio chunks.
2. **Speech-to-Text**:
   - **Online (Default)**: Uses Google's Speech Recognition API. It first attempts to recognize Indonesian (`id-ID`) and falls back to English (`en-US`).
   - **Offline (Optional)**: Uses a local Vosk model (`vosk-model-small-id-0.22`) for zero-latency, private recognition.
3. **Command Mapping**: The recognized text is compared against a pre-computed dictionary of keywords (`config.py`). The mapping uses an optimized $O(1)$ exact match and an $O(K)$ substring search (sorted by length descending) to handle overlapping commands accurately (e.g., distinguishing between "lanjut" and "lanjutkan").

### Presentation Controller

The controller acts as the bridge between the detected commands and your operating system. It translates logical commands (like "Next") into physical keyboard strokes.

**How it works:**
1. **Application Detection**: Uses Windows APIs (`win32gui`, `psutil`) to identify the currently active window and process.
2. **Profile Matching**: Maps the detected application (e.g., `powerpnt.exe` or a browser tab containing "Google Slides") to a specific keyboard profile.
3. **Command Execution**: Uses `pyautogui` to simulate the correct keystroke for the active application (e.g., `Right Arrow` for PowerPoint or `Space` for Google Slides).
4. **Debouncing**: Enforces a minimum delay (`debounce_time`) between commands to prevent accidental double-triggers (e.g., skipping two slides with one swipe).
