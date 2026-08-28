# How It Works

This explanation section outlines the underlying architecture and technology stack of the Presentation Control Tool. It aims to help developers understand the core components and how they interact.

---

## Architecture Overview

The Presentation Control Tool bridges the gap between physical actions (hand gestures, speech) and software interactions (keyboard commands) using three main modules: the Gesture Detector, the Voice Recognizer, and the Presentation Controller.

### Gesture Detector (`gesture_detector.py`)

This module captures the video feed from your webcam and processes it using computer vision techniques via the `opencv-python` (cv2) library.

1. **Capture**: It retrieves frames directly from the webcam (`cv2.VideoCapture`).
2. **Preprocessing**: The frame is converted to grayscale, resized to reduce processing overhead, and blurred (`cv2.GaussianBlur`) to minimize noise.
3. **Motion Detection**: It compares the current frame with the previous one (`cv2.absdiff`) to identify moving objects.
4. **Contour Extraction**: It thresholds the difference and finds contours (`cv2.findContours`) to isolate the hand.
5. **Logic**: By calculating the centroid of the largest contour and tracking its movement over time, the detector determines the direction of swipes and maps them to predefined commands. It also employs debouncing logic to prevent multiple commands from being sent for a single continuous motion.

### Voice Recognizer (`voice_recognizer.py`)

This module listens to audio input from your microphone and converts it into text commands.

1. **Capture**: It records audio continuously in a background thread using `pyaudio` and `SpeechRecognition`.
2. **Detection Engine**: The tool attempts to recognize the speech using either the online Google Speech Recognition API or an offline Vosk model, depending on the user's configuration.
3. **Command Mapping**: The recognized text is passed through a command mapping algorithm. It checks for specific keywords in English or Indonesian (e.g., "next", "lanjut") and maps them to standard presentation commands (e.g., "next slide").

### Presentation Controller (`controller.py`)

This module receives the parsed commands from the Gesture Detector and Voice Recognizer and translates them into keyboard inputs that control the presentation software.

1. **App Detection**: It uses `psutil` and `win32gui` (on Windows) to determine which application is currently active and focused (e.g., PowerPoint, a web browser running Google Slides).
2. **Command Translation**: It looks up the specific keyboard shortcut for the active application based on the received command (e.g., "next" maps to the right arrow key for PowerPoint).
3. **Execution**: It simulates the corresponding key press using the `pyautogui` library, effectively controlling the presentation without any physical interaction from the user.

## Why This Matters

By abstracting these technologies into a single, cohesive tool, we eliminate the need for physical clickers and enable more expressive, hands-free presentations. The modular design also makes it easy to add support for new gestures, voice commands, or presentation applications.