## 2024-05-23 - [Audio Stream Overhead]
**Learning:** Initializing `sr.Microphone` inside a loop causes significant latency due to repeated stream opening/closing (expensive OS operation).
**Action:** Always initialize `Microphone` context outside the loop and handle `WaitTimeoutError` internally to keep the stream open.
