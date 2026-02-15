## 2025-10-26 - [Voice Recognition Latency]
**Learning:** `speech_recognition`'s `Microphone` context manager opens/closes the PyAudio stream. Using it inside a tight loop adds significant latency and CPU overhead due to repetitive stream setup.
**Action:** When using `recognizer.listen()` in a loop, open the microphone context once outside the loop to maintain a persistent stream.
