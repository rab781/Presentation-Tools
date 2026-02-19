## 2026-02-19 - Voice Recognition Loop Optimization
**Learning:** In `VoiceRecognizer._listen_loop`, repeatedly entering/exiting the `sr.Microphone()` context manager inside a tight loop causes expensive audio stream re-initialization on every iteration (every 1-3 seconds). This significantly impacts CPU usage and latency.
**Action:** Always place the `with self.microphone as source:` context manager OUTSIDE the main listening loop to keep the audio stream open continuously. Use exception handling (`sr.WaitTimeoutError`) to manage silent periods without breaking the stream.
