## 2024-03-03 - [Microphone Stream Initialization Bottleneck]
**Learning:** `VoiceRecognizer._listen_loop` re-initializes the microphone context (`with self.microphone as source:`) on every iteration. This introduces significant overhead, causing choppy listening, missed words, and excessive system calls, especially when a timeout occurs or speech isn't immediately detected. This is a common pattern that hurts performance in speech recognition loops.
**Action:** Optimize the `_listen_loop` by keeping the microphone context open continuously. Introduce an inner loop for continuous listening that only breaks and re-initializes the stream on critical errors.

## 2025-01-01 - [Removed redundant UI rendering in gesture loop]
**Learning:** `cv2.putText` operations inside the frame processing loop introduce unnecessary overhead, especially when the UI is already centralized elsewhere (`main.py` via `_draw_ui`). Redundant rendering blocks the critical path of gesture detection.
**Action:** Always separate core processing logic (like computer vision detection) from UI rendering, and remove redundant drawing operations to maximize frame rate.
