## 2024-05-22 - Persistent Audio Stream in Loops
**Learning:** Re-initializing `sr.Microphone` context inside a `while` loop (on every timeout) causes significant overhead and potential audio gaps.
**Action:** Move the context manager outside the loop and handle `WaitTimeoutError` inside to keep the stream open.
