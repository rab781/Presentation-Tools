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
        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]

        # Resize for processing if needed
        proc_w = int(width * self.processing_scale)
        proc_h = int(height * self.processing_scale)
        
        # Convert to grayscale for motion detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_small = cv2.resize(gray, (proc_w, proc_h))
        gray_small = cv2.GaussianBlur(gray_small, (21, 21), 0)
        
        gesture_command = None
        
        if self.prev_frame is not None:
            # Compute difference
            frame_delta = cv2.absdiff(self.prev_frame, gray_small)
            # ⚡ OPTIMIZATION: Using dst parameter to perform thresholding and dilation in-place
            # on the frame_delta array. This prevents allocating multiple intermediate
            # images during the critical hot-path frame loop, reducing memory pressure
            # and garbage collection overhead.
            cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY, dst=frame_delta)
            cv2.dilate(frame_delta, None, iterations=2, dst=frame_delta)
            thresh = frame_delta
            
            # Find contours
            # ⚡ OPTIMIZATION: OpenCV 4+ does not modify the source image, making .copy() redundant.
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Find largest contour
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Scale threshold: 5000 is for 640x480.
                min_area = 5000 * (self.processing_scale ** 2)

                if cv2.contourArea(largest_contour) > min_area:  # Minimum area threshold
                    # Get center of motion
                    M = cv2.moments(largest_contour)
                    if M["m00"] != 0:
                        cx_small = int(M["m10"] / M["m00"])
                        cy_small = int(M["m01"] / M["m00"])

                        # Scale back to original coordinates
                        cx = int(cx_small / self.processing_scale)
                        cy = int(cy_small / self.processing_scale)
                        
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
                            scaled_contour = largest_contour * (1.0 / self.processing_scale)
                            scaled_contour = scaled_contour.astype(np.int32)
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
