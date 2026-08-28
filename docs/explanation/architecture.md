# Explanation: Architecture

The Presentation Control Tool operates through a pipeline of distinct modules that handle input detection, command interpretation, and application control. Understanding this architecture helps you troubleshoot issues and develop custom features.

## Core Modules

The application is composed of four primary components:

1. **`main.py` (Application Coordinator)**: Manages the execution loop, UI rendering, mode switching, and initialization of the input modules.
2. **`gesture_detector.py` (Computer Vision)**: Captures webcam frames, processes them to detect hand gestures, and translates motions into commands.
3. **`voice_recognizer.py` (Speech-to-Text)**: Listens to the microphone stream in a background thread, processes audio using online or offline models, and translates speech into commands.
4. **`controller.py` (Application Controller)**: Translates abstract commands into specific keyboard shortcuts and simulates keystrokes using PyAutoGUI.

## Execution Flow

1. **Initialization**: The `main.py` script loads user configurations via the `ConfigManager` and instantiates the enabled input modules (Gesture, Voice, or both).
2. **Detection Loop**:
   - The **Gesture Detector** processes camera frames synchronously in the main loop using OpenCV. It applies optimizations like frame downscaling, grayscale conversion, and double-buffering to minimize latency.
   - The **Voice Recognizer** continuously listens to the microphone in a separate daemon thread to avoid blocking the visual rendering loop. It queues detected commands for the main loop to process.
3. **Command Translation**: When a module detects an action (e.g., a right swipe or the word "next"), it maps it to a unified abstract command (e.g., `next`).
4. **Contextual Execution**: The `PresentationController` checks the currently active window (e.g., PowerPoint, Chrome) using `win32process` and `psutil`. It maps the abstract command to the correct keyboard shortcut for that specific application and simulates the keystrokes.

## Performance Optimizations

The tool incorporates several performance engineering principles:

- **In-Place Mutations**: OpenCV operations use the `dst` parameter to modify arrays in-place, preventing expensive memory allocations per frame.
- **Background Threading**: Blocking operations, such as audio playback (`winsound.Beep`) and continuous microphone listening, run in separate threads to maintain high UI framerates.
- **Process Resolution Caching**: The controller caches the detected application process based on the window handle and title, avoiding expensive system calls on every command execution.
- **Configuration-Driven Logic**: The voice recognizer skips unnecessary API calls based on the configured language, reducing latency.
