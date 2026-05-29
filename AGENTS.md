# Presentation Control Tool - Agent Guidelines

This repository contains `AGENTS.md` to document core architectural patterns, performance optimization strategies, and testing requirements specific to this codebase. All automated agents and developers must adhere to these guidelines to maintain performance and avoid regressions.

## ⚡ Performance Optimizations

### OpenCV Array Operations
* **In-place Operations (`dst` parameter):** Operations like `cv2.threshold`, `cv2.dilate`, `cv2.GaussianBlur`, `cv2.addWeighted`, and `cv2.absdiff` should utilize the `dst` parameter to perform in-place array modifications (e.g., `cv2.threshold(..., dst=frame_delta)`). This avoids unnecessary memory allocations and garbage collection overhead in hot-path loops.
* **Caller Array Safety:** Do not pre-allocate and return shared class-level buffers (e.g., `self.flip_buffer = np.empty_like(frame)`) for operations like `cv2.flip` in detector methods that return the frame to the caller. Do not use the `dst` parameter for OpenCV functions that mutate arrays passed by the caller, as it creates a mutable shared reference that can cause dangerous side effects if the caller modifies it.
* **Double Buffering:** When optimizing functions that generate sequential frame data (like `cv2.resize` acting as a `prev_frame`), use a double-buffering scheme (e.g., `buffers[0]` and `buffers[1]`) alongside the `dst` parameter to prevent inside-loop array allocations without inadvertently corrupting historical states required for operations like `cv2.absdiff`.
* **`cv2.findContours`:** OpenCV 4+ no longer modifies the source image. Using `.copy()` on the input image is redundant and wastes CPU cycles and memory allocations per frame. Remove `.copy()` calls.

### Voice Recognition
* **Microphone Context Management:** Avoid stream initialization latency by managing the microphone context (`with self.microphone as source:`) in an outer loop. Use an inner loop to continuously listen, catching `sr.WaitTimeoutError` to maintain the open stream. Only break the inner loop on critical errors to re-initialize the context.
* **External API Calls:** Avoid hardcoded sequential fallback API calls (e.g., trying one language endpoint and waiting for a timeout before trying another). Check active configuration preferences first to conditionally skip unnecessary blocking network requests and reduce latency, while ensuring you fall back safely ("fail open") if the configuration value is unrecognized.
* **Vosk Recognizer Caching:** When caching and reusing a single `vosk.KaldiRecognizer` instance to avoid per-frame instantiation overhead, explicitly call `.Reset()` before processing a new audio segment to prevent stateful cross-utterance bleeding.
* **Dictionary Lookups:** Do not iterate over dictionary values for reverse lookups on every evaluation. Pre-compute a `command_map` dictionary and a list of `all_keywords` sorted by length (descending) during `__init__`. The lookup uses an O(1) exact match followed by an O(K) substring search, ensuring faster processing and correct prioritization of overlapping keywords (e.g., 'lanjutkan' vs 'lanjut').

### UI and Main Loop
* **Pre-allocate Status UI:** In the application loop, continuously rendering static or blank UI frames (e.g., in voice-only or paused modes) by creating new NumPy arrays (like `np.zeros()`) causes significant memory allocation overhead. Optimize this by pre-allocating the canvas once and clearing it in-place using `.fill(0)` before drawing.
* **Non-blocking Execution:** Run synchronous operations like `winsound.Beep` asynchronously in a background thread to eliminate blocking behavior in the main thread.
* **Queue Management:** In threaded producer-consumer queues, do not clear the queue by reassigning the variable (e.g., `self.command_queue = queue.Queue()`). This desynchronizes threads holding references to the old instance; always empty the existing queue instance in-place.
* **Debouncing Logic:** Do not evaluate rate-limiting/debouncing conditions in producer methods before enqueuing. These conditions must be evaluated by the consumer thread at execution time to prevent concurrency bugs and broken debounce logic.
* **Python Built-ins:** Do not replace C-optimized Python built-ins (like `max(..., key=...)`) with manual Python `for` loops in an attempt to optimize performance, except in very specific cases where multiple passes over small data structures can be manually combined.

## 🧪 Testing and Mocks

* **Command to Run Tests:** Execute all unit tests within the repository using the command: `PYTHONPATH=. python -m unittest discover tests`.
* **Missing Dependencies:** Heavy or optional dependencies (`pyautogui`, `cv2`, `numpy`, `speech_recognition`, `pyaudio`, `vosk`, `win32gui`, `win32process`, `psutil`, `winsound`) might be missing in the environment. Tests must mock these modules in `sys.modules` before importing project code.
* **Mocking OpenCV (`cv2`):**
  * Operations that return modified frames (like `cv2.flip`, `cv2.resize`, `cv2.GaussianBlur`) must be mocked to return an object with a `.shape` attribute.
  * If testing in-place operations with the `dst` parameter, the mock must explicitly set `dst.shape = src.shape` before returning `dst` to prevent tuple unpacking errors in downstream logic. Ensure the mock side-effect functions explicitly accept the `dst` keyword argument.
  * `benchmark_gesture.py` requires functional mocks for `cv2.contourArea` and `cv2.moments` for successful execution when OpenCV is not present. Use `MagicMock` directly to simplify the code instead of empty mock function definitions.
* **Exception Handling:** Always prefer `except Exception:` over bare `except:` clauses to ensure that system-level signals like `KeyboardInterrupt` and `SystemExit` are not accidentally suppressed.

## 📝 Documentation Standards (Technical Writer Guidelines)

* **Divio Documentation System:** Separate content into tutorials (learning-oriented), how-to guides (task-oriented), reference (information-oriented), and explanation (understanding-oriented) without mixing these types.
* **Persona:** Adopt the Technical Writer persona: use second person ('you'), present tense, and active voice. Ensure all code examples run and assume no prior context. Lead explanations with user outcomes rather than features.
* **Clarity:** Be explicit and specific about failure states and troubleshooting. Ruthlessly cut any sentence that does not help the reader do or understand something.
* **Versioning:** Version everything (deprecate old docs, never delete) and maintain one concept per section (do not mix installation, configuration, and usage).
* **README Structure:** README files must pass the '5-second test' (what, why, how) and structurally include: Why This Exists, Quick Start, Installation, Usage, Configuration/API, Contributing, and License.
* **Docs as Code:** Every new feature must ship with documentation, and every breaking change requires a migration guide.

## 🛑 Repository Policies
* Do not commit temporary developer scripts or mock testing files (e.g., `benchmark_in_place.py`, `fix_tests.py`) to the repository; always clean them up before requesting code review or creating a pull request.
