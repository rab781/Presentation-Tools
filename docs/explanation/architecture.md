# System Architecture

The Presentation Control Tool is built on a modular, hybrid architecture designed for real-time responsiveness and low latency. It bridges computer vision, speech recognition, and operating system automation.

## The Hybrid Processing Loop

At the core of the application (`main.py`) is a concurrent processing loop that manages multiple input streams without blocking the main thread.

1. **Vision Pipeline**: A continuous loop reads frames from the webcam, processes them through the `GestureDetector`, and applies heuristics to identify specific hand shapes and motions.
2. **Audio Pipeline**: Background threads, managed by the `VoiceRecognizer`, continuously listen to microphone input, segmenting audio based on silence thresholds, and dispatching speech-to-text processing asynchronously.
3. **Command Orchestration**: Both pipelines yield unified actions (e.g., "next", "previous") which are fed into a central command queue.

## Input Modalities

### Computer Vision (`gesture_detector.py`)

The gesture detection system prioritizes speed. It utilizes optimized computer vision techniques (like frame scaling and direct contour area calculations) to maintain high frame rates even on lower-end hardware, bypassing the need for heavy machine learning models like MediaPipe.

### Speech Recognition (`voice_recognizer.py`)

The voice recognition module implements a bilingual fallback strategy:
- **Cloud-First**: By default, it uses Google's robust cloud API for high accuracy.
- **Offline Fallback**: Network interruptions or explicit user configurations trigger the local Vosk model, ensuring the presentation flow is never broken by an internet outage.

## Application Automation (`controller.py`)

Once a command is registered, the `PresentationController` takes over. It identifies the currently active window (e.g., Chrome running Google Slides vs. native PowerPoint) and translates the generic command into the specific keyboard shortcut expected by that application. It includes a debouncing mechanism to prevent a single swipe from advancing multiple slides at once.
