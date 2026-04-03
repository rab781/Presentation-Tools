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

## 2025-12-18 - [Avoid in-place array operations that mutate caller arrays]
**Learning:** In-place mutations of caller-provided arrays (e.g., `cv2.flip(frame, 1, dst=frame)`) are dangerous and can cause side-effects where the caller expects the original array structure.
**Action:** Do not use the `dst` parameter for OpenCV functions that mutate arrays passed by the caller.

## 2025-12-18 - [In-place array operations with OpenCV dst parameter inside functions]
**Learning:** We can use the `dst` parameter in operations that create intermediate representations such as `cv2.threshold` and `cv2.dilate`.
**Action:** We will use `dst=frame_delta` in `cv2.threshold` and `dst=thresh` in `cv2.dilate` to perform these operations in place.

## 2025-12-18 - [In-place array operations with OpenCV dst parameter inside cv2.GaussianBlur]
**Learning:** `cv2.GaussianBlur` allocates a new array by default, but can perform operations in-place by passing the `dst` parameter. This reduces expensive full-frame memory allocations and reduces garbage collection overhead per frame.
**Action:** Always use the `dst` parameter (e.g., `dst=gray_small`) for OpenCV functions when the input array can be safely mutated in-place such as in `cv2.GaussianBlur(gray_small, (21, 21), 0, dst=gray_small)`.

## 2025-12-18 - [In-place array operations with OpenCV absdiff]
**Learning:** `cv2.absdiff` allocates a new array by default, but can perform operations in-place by passing the `dst` parameter. When computing frame differences (e.g., `frame_delta = cv2.absdiff(self.prev_frame, gray_small)`), the old frame buffer is often no longer needed and can be repurposed as the destination array (`dst=self.prev_frame`). This reduces expensive memory allocations per frame and lowers garbage collection overhead.
**Action:** Use the `dst` parameter (e.g., `dst=self.prev_frame`) for `cv2.absdiff` when the input array can be safely overwritten.

## 2025-12-19 - [Double-buffering to prevent allocation in OpenCV operations]
**Learning:** `cv2.resize` and `cv2.cvtColor` allocate new arrays by default. While they accept the `dst` parameter in Python, using `dst` for functions generating sequential frame data (like `cv2.resize` acting as `prev_frame`) can inadvertently corrupt motion detection history if the buffer is overwritten in the next iteration before comparison.
**Action:** Use a double-buffering array scheme (e.g. `buffers[0]` and `buffers[1]`) alongside the `dst` parameter to prevent array allocations inside hot-loops while safely preserving previous state for `cv2.absdiff` and similar operations.
## 2025-12-20 - [Pre-allocate UI status frame]
**Learning:** In the `main.py` application loop, continuously rendering static or blank UI frames (e.g., in voice-only or paused modes) by creating new NumPy arrays (like `np.zeros()`) causes significant memory allocation overhead.
**Action:** Optimize this by pre-allocating the canvas once and clearing it in-place using `.fill(0)` before drawing.

## 2025-12-21 - [Prevent redundant external API calls in loops]
**Learning:** Hardcoded sequential external API calls (e.g., trying an Indonesian Speech-to-Text API and waiting for it to timeout and throw an exception before trying English) cause significant latency (1-2 seconds) per recognition loop iteration.
**Action:** Always check the configuration first to respect the user's preference. Conditionally skip unnecessary, expensive network requests to reduce latency, while ensuring you fall back safely ("fail open") to default behavior if the configuration value is unrecognized.
