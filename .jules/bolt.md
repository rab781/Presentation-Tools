## 2025-12-17 - Voice Recognizer Microphone Context Optimization
**Learning:** In `voice_recognizer.py`, the `_listen_loop` opens the microphone context manager (`with self.microphone as source:`) continuously inside the `while self.is_listening:` loop. Opening and closing the audio stream on every single timeout iteration (every 1 second when silent) adds unnecessary overhead and latency.
**Action:** Optimize `_listen_loop` by using an outer loop to manage the microphone context (`with self.microphone as source:`), and an inner loop (`while self.is_listening:`) to continuously listen for audio without closing the stream. Catch `sr.WaitTimeoutError` inside the inner loop to continue listening seamlessly. For other exceptions, break out of the inner loop to re-initialize the microphone context.
## 2024-03-03 - [Microphone Stream Initialization Bottleneck]
**Learning:** `VoiceRecognizer._listen_loop` re-initializes the microphone context (`with self.microphone as source:`) on every iteration. This introduces significant overhead, causing choppy listening, missed words, and excessive system calls, especially when a timeout occurs or speech isn't immediately detected. This is a common pattern that hurts performance in speech recognition loops.
**Action:** Optimize the `_listen_loop` by keeping the microphone context open continuously. Introduce an inner loop for continuous listening that only breaks and re-initializes the stream on critical errors.

## 2025-01-01 - [Removed redundant UI rendering in gesture loop]
**Learning:** `cv2.putText` operations inside the frame processing loop introduce unnecessary overhead, especially when the UI is already centralized elsewhere (`main.py` via `_draw_ui`). Redundant rendering blocks the critical path of gesture detection.
**Action:** Always separate core processing logic (like computer vision detection) from UI rendering, and remove redundant drawing operations to maximize frame rate.

## 2025-05-16 - [Redundant array copy in OpenCV 4+ findContours]
**Learning:** `cv2.findContours` in OpenCV 4 and newer no longer modifies the source image. Using `.copy()` on the input image is redundant and wastes CPU cycles and memory allocations per frame.
**Action:** Remove `.copy()` calls when passing thresholded images to `cv2.findContours` to improve frame processing speed and reduce garbage collection overhead.
## 2025-05-18 - [Non-blocking audio commands]
**Learning:** The `PresentationController._play_sound_effect` method in `controller.py` used `winsound.Beep`, which is synchronous and blocks the thread for the duration of the beep (100ms). This blocked the main control loop and impacted application responsiveness when executing commands.
**Action:** Run synchronous sound operations like `winsound.Beep` asynchronously in a background thread using `threading.Thread(target=winsound.Beep, args=(frequency, duration), daemon=True).start()` to eliminate blocking behavior.

## 2025-05-18 - [In-place array operations with OpenCV dst parameter]
**Learning:** OpenCV operations like `cv2.flip` and `cv2.addWeighted` allocate new arrays by default, but can perform operations in-place by passing the `dst` parameter. This prevents expensive full-frame memory allocations and reduces garbage collection overhead per frame.
**Action:** Always use the `dst` parameter (e.g., `dst=frame` or `dst=roi`) for OpenCV functions when the input array can be safely mutated in-place.
## 2025-05-18 - [O(1) dictionary lookup instead of O(N) looping]
**Learning:** In `voice_recognizer.py`, `_map_command_to_action` previously iterated over the entire `VOICE_COMMANDS` dictionary values for every text evaluation. This is highly inefficient. Pre-computing a `command_map` dictionary and a list of `all_keywords` sorted by length descending during `__init__` enables an $O(1)$ exact match and $O(K)$ substring search, ensuring faster processing and correct prioritization of overlapping keywords (e.g., 'lanjutkan' vs 'lanjut').
**Action:** Avoid looping over dictionary values for reverse lookups. Pre-compute mappings and sort substrings by length descending to optimize text command mapping performance and guarantee correct keyword precedence.
