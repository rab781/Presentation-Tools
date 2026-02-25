## 2025-12-17 - Voice Recognition Stream Optimization
**Learning:** `speech_recognition.Microphone` context manager re-opens the audio stream on entry. Using it inside a `while` loop causes constant stream setup/teardown overhead, significantly impacting performance and CPU usage.
**Action:** Always wrap the listening loop *inside* the `with microphone` block, handling `WaitTimeoutError` to keep the stream alive.
