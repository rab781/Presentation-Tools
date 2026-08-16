"""
Simplified Hand Gesture Detection Module
This version works without MediaPipe for testing purposes
Uses simple computer vision techniques
"""

import cv2
import numpy as np
import time
from typing import Optional, Tuple
from config import GESTURE_CONFIG, GESTURE_COMMANDS


class GestureDetector:
    """Simple gesture detector using basic computer vision"""
    
    def __init__(self, camera_index=0, processing_scale=0.5):
        self.camera_index = camera_index
        self.processing_scale = processing_scale
        self.cap = None

        # ⚡ OPTIMIZATION: Pre-calculate constants
        # Calculate these once during initialization instead of per-frame
        # to reduce floating point arithmetic overhead in the hot loop.
        self.min_area = 5000 * (self.processing_scale ** 2)
        self.inv_processing_scale = 1.0 / self.processing_scale if self.processing_scale != 0 else 1.0
        
        # ⚡ OPTIMIZATION: Pre-calculate contour scaling function
        # Scaling the contour array directly using a float multiplier is expensive because
        # it promotes the int array to float, requiring a subsequent astype(int32) cast.
        # If the inverse scale is an integer (and especially a power of 2 like 2 for a 0.5 scale),
        # we can use significantly faster operations like bitwise shifts or integer multiplication.
        import math
        if self.inv_processing_scale.is_integer():
            inv_scale_int = int(self.inv_processing_scale)
            if inv_scale_int > 0 and (inv_scale_int & (inv_scale_int - 1)) == 0:
                # Power of 2: Use bitwise left shift (fastest)
                shift_val = int(math.log2(inv_scale_int))
                self.scale_contour = lambda contour: contour << shift_val
            else:
                # Integer: Use integer multiplication (faster than float)
                self.scale_contour = lambda contour: contour * inv_scale_int
        else:
            # Float: Fallback to float multiplication and casting
            self.scale_contour = lambda contour: (contour * self.inv_processing_scale).astype(np.int32)

        # Gesture tracking
        self.last_gesture = None
        self.last_gesture_time = 0
        self.gesture_history = []
        self.history_size = 5
        
        # For simple motion detection
        self.prev_frame = None
        self.prev_center = None
        
    def start(self):
        """Start camera capture"""
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera {self.camera_index}")
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
    
    def stop(self):
        """Stop camera capture"""
        if self.cap:
            self.cap.release()
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Read a frame from camera"""
        if not self.cap:
            return False, None
        return self.cap.read()
    
    def detect_gesture(self, frame: np.ndarray, draw_landmarks=True) -> Tuple[Optional[str], np.ndarray]:
        """
        Detect simple gestures using motion detection
        Returns: (gesture_command, annotated_frame)
        """
        # ⚡ OPTIMIZATION: Pre-allocate buffer for cv2.flip
        # cv2.flip allocates a new array by default. By passing a pre-allocated
        # buffer to the `dst` parameter, we avoid an expensive memory allocation
        # (e.g., 640x480x3 bytes = ~900KB) per frame, reducing garbage collection overhead.
        # We do not use dst=frame to avoid mutating the caller's array.
        if not hasattr(self, 'flip_buffer') or self.flip_buffer.shape != frame.shape:
            self.flip_buffer = np.empty_like(frame)
        frame = cv2.flip(frame, 1, dst=self.flip_buffer)

        height, width = frame.shape[:2]

        # Resize for processing if needed
        proc_w = int(width * self.processing_scale)
        proc_h = int(height * self.processing_scale)
        
        # ⚡ OPTIMIZATION: Convert to grayscale before resizing
        # Converting to grayscale first is highly vectorized and fast. Resizing an image
        # is an interpolation operation that scales heavily with the number of channels.
        # Doing grayscale first significantly reduces the interpolation overhead.

        if not hasattr(self, 'gray_full_buffer') or self.gray_full_buffer.shape[:2] != (height, width):
            self.gray_full_buffer = np.empty((height, width), dtype=getattr(frame, 'dtype', np.uint8))

        gray_full = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, dst=self.gray_full_buffer)

        # ⚡ OPTIMIZATION: Double-buffering for the downscaled grayscale image
        # We use a double-buffering scheme for the final downscaled frame because `self.prev_frame`
        # (from the previous loop) must be preserved for motion detection via `cv2.absdiff`,
        # which then mutates it in-place.
        if not hasattr(self, 'gray_small_buffers'):
            self.gray_small_buffers = [None, None]
            self.buffer_idx = 0

        curr_buffer = self.gray_small_buffers[self.buffer_idx]
        if curr_buffer is None or curr_buffer.shape[:2] != (proc_h, proc_w):
            curr_buffer = np.empty((proc_h, proc_w), dtype=np.uint8)
            self.gray_small_buffers[self.buffer_idx] = curr_buffer

        # Downscale the grayscale image
        gray_small = cv2.resize(gray_full, (proc_w, proc_h), dst=curr_buffer)

        # Swap buffer index for the next frame
        self.buffer_idx = 1 - self.buffer_idx

        # ⚡ OPTIMIZATION: In-place array operations
        # By passing `dst=gray_small` to cv2.GaussianBlur, we perform the blur directly
        # in the memory of the `gray_small` array, avoiding an intermediate array allocation.
        gray_small = cv2.GaussianBlur(gray_small, (21, 21), 0, dst=gray_small)
        
        gesture_command = None
        
        if self.prev_frame is not None:
            # Compute difference
            # ⚡ OPTIMIZATION: In-place array operations
            # We no longer need the old prev_frame, so we can use it as the destination
            # array for the absdiff result, avoiding a new array allocation per frame.
            try:
                frame_delta = cv2.absdiff(self.prev_frame, gray_small, dst=self.prev_frame)
            except TypeError:
                # Fallback for mocks/local implementations of cv2.absdiff that do not
                # accept the `dst` keyword argument (e.g., simple two-arg mocks).
                frame_delta = cv2.absdiff(self.prev_frame, gray_small)
                # We lose the in-place optimization here, but preserve behavior.
                self.prev_frame = frame_delta
            # ⚡ OPTIMIZATION: In-place array operations
            # By passing `dst=frame_delta` to cv2.threshold and `dst=thresh` to cv2.dilate,
            # we reuse existing memory buffers instead of allocating new arrays. This reduces
            # expensive memory allocations per frame and lowers garbage collection overhead.
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY, dst=frame_delta)[1]
            thresh = cv2.dilate(thresh, None, iterations=2, dst=thresh)
            
            # Find contours
            # ⚡ OPTIMIZATION: OpenCV 4+ does not modify the source image, making .copy() redundant.
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Find largest contour
                largest_contour = max(contours, key=cv2.contourArea)
                
                # ⚡ OPTIMIZATION: Cache contour area
                # Calculate the area once and store it in a local variable to prevent
                # repeated evaluations of cv2.contourArea in downstream validation logic.
                largest_area = cv2.contourArea(largest_contour)

                if largest_area > self.min_area:  # Minimum area threshold
                    # Get center of motion
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    cx_small = int(x + w // 2)
                    cy_small = int(y + h // 2)

                    # Scale back to original coordinates
                    cx = int(cx_small * self.inv_processing_scale)
                    cy = int(cy_small * self.inv_processing_scale)

                    # Detect swipe gestures based on movement
                    if self.prev_center is not None:
                        dx = cx - self.prev_center[0]
                        dy = cy - self.prev_center[1]
                        
                        # Horizontal swipe
                        if abs(dx) > 100 and abs(dy) < 50:
                            if dx > 0:
                                gesture = "SWIPE_RIGHT"
                            else:
                                gesture = "SWIPE_LEFT"
                            
                            if self._validate_gesture(gesture):
                                gesture_command = GESTURE_COMMANDS.get(gesture)

                    self.prev_center = (cx, cy)

                    # Draw visualization
                    if draw_landmarks:
                        cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
                        # Scale contour for drawing
                        scaled_contour = self.scale_contour(largest_contour)
                        cv2.drawContours(frame, [scaled_contour], -1, (0, 255, 0), 2)
        
        self.prev_frame = gray_small
        
        return gesture_command, frame
    
    def _validate_gesture(self, gesture: str) -> bool:
        """Validate gesture with debouncing"""
        current_time = time.time()
        
        # Check debounce time
        if (self.last_gesture == gesture and 
            current_time - self.last_gesture_time < 1.0):  # 1 second debounce
            return False
        
        self.last_gesture = gesture
        self.last_gesture_time = current_time
        return True
    
    def get_fps(self) -> float:
        """Get current FPS"""
        if self.cap:
            return self.cap.get(cv2.CAP_PROP_FPS)
        return 0.0
    
    def is_active(self) -> bool:
        """Check if camera is active"""
        return self.cap is not None and self.cap.isOpened()
