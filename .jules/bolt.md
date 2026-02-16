## 2024-05-22 - Voice Recognition Optimization
**Learning:** Re-opening the microphone stream on every iteration of a listening loop is a significant performance bottleneck due to OS-level audio device initialization overhead.
**Action:** Use the `Microphone` context manager outside the loop to keep the stream open. Handle `WaitTimeoutError` inside the loop to continue listening without resetting the stream.
