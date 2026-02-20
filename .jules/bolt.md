## 2024-05-22 - Voice Recognition Loop Optimization
**Learning:** The `VoiceRecognizer._listen_loop` was re-opening the microphone stream (via `pyaudio`) on every iteration because the context manager `with self.microphone` was inside the `while` loop. This caused significant overhead and potential latency.
**Action:** When implementing continuous listening loops with `speech_recognition`, always ensure the microphone context manager is outside the loop to keep the stream open.
