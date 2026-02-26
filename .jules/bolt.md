## 2024-10-24 - Voice Recognition Loop Optimization
**Learning:** `speech_recognition.Microphone` context manager incurs significant overhead by opening/closing the PyAudio stream on every iteration (e.g., every 1-second timeout).
**Action:** Move the context manager (`with self.microphone as source:`) outside the `while` loop. Catch `WaitTimeoutError` inside the loop to persist the stream. Ensure the outer loop catches critical errors to restart the stream if needed.
