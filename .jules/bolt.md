# Bolt's Journal

## 2025-10-26 - Speech Recognition Stream Overhead
**Learning:** Initializing the audio stream (via `speech_recognition.Microphone` context manager) is an expensive operation that involves OS-level audio device negotiation. Doing this inside a tight loop causes significant latency and potential audio dropouts.
**Action:** Always hoist the `with microphone as source:` context manager outside of the main processing loop. Use an inner loop for continuous listening, catching `WaitTimeoutError` to keep the stream alive during silence. Ensure proper exception handling breaks the inner loop to force stream re-initialization only on critical errors.
