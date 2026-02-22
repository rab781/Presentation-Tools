## 2026-02-22 - [Voice Recognition Optimization]
**Learning:** Reusing `speech_recognition.Microphone` context manager significantly reduces CPU overhead and latency by avoiding repeated audio stream initialization.
**Action:** Always check hardware device lifecycle (open/close) inside loops; move initialization outside the loop when possible.
