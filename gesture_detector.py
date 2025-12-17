"""
Hand Gesture Detection Module using MediaPipe
Detects various hand gestures for presentation control
"""

import cv2
import mediapipe as mp
import numpy as np
import time
from typing import Optional, Tuple, Dict
from config import GESTURE_CONFIG, GESTURE_COMMANDS


class GestureDetector:
    """Detects hand gestures using MediaPipe Hands"""
    
    def __init__(self, camera_index=0):
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Setup hand detector
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=GESTURE_CONFIG["max_hands"],
            min_detection_confidence=GESTURE_CONFIG["min_detection_confidence"],
            min_tracking_confidence=GESTURE_CONFIG["min_tracking_confidence"]
        )
        
        # Camera setup
        self.camera_index = camera_index
        self.cap = None
        
        # Gesture tracking
        self.last_gesture = None
        self.last_gesture_time = 0
        self.gesture_start_time = {}
        self.prev_hand_position = None
        
        # Gesture history for debouncing
        self.gesture_history = []
        self.history_size = 5
        
    def start(self):
        """Start camera capture"""
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera {self.camera_index}")
        
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
    def stop(self):
        """Stop camera capture"""
        if self.cap:
            self.cap.release()
        self.hands.close()
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Read a frame from camera"""
        if not self.cap:
            return False, None
        return self.cap.read()
    
    def detect_gesture(self, frame: np.ndarray, draw_landmarks=True) -> Tuple[Optional[str], np.ndarray]:
        """
        Detect gesture from frame
        Returns: (gesture_command, annotated_frame)
        """
        # Flip frame horizontally for mirror view
        frame = cv2.flip(frame, 1)
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame
        results = self.hands.process(rgb_frame)
        
        gesture_command = None
        
        # If hand detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                if draw_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
                
                # Detect gesture
                gesture = self._recognize_gesture(hand_landmarks, frame.shape)
                
                if gesture:
                    # Apply debouncing and hold time
                    if self._validate_gesture(gesture):
                        gesture_command = GESTURE_COMMANDS.get(gesture)
        
        return gesture_command, frame
    
    def _recognize_gesture(self, hand_landmarks, frame_shape) -> Optional[str]:
        """Recognize specific gestures from hand landmarks"""
        
        # Extract landmark coordinates
        landmarks = []
        for lm in hand_landmarks.landmark:
            landmarks.append((lm.x, lm.y, lm.z))
        
        # Get key points
        wrist = landmarks[0]
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Get finger base points
        index_base = landmarks[5]
        middle_base = landmarks[9]
        ring_base = landmarks[13]
        pinky_base = landmarks[17]
        
        # Calculate hand center
        hand_center = np.mean(landmarks, axis=0)
        
        # Detect swipe gestures
        swipe = self._detect_swipe(hand_center)
        if swipe:
            return swipe
        
        # Detect static gestures
        
        # OPEN PALM - all fingers extended
        if self._all_fingers_extended(landmarks):
            return "OPEN_PALM"
        
        # CLOSED FIST - all fingers closed
        if self._all_fingers_closed(landmarks):
            return "CLOSED_FIST"
        
        # THUMB UP
        if self._is_thumb_up(landmarks):
            return "THUMB_UP"
        
        # THUMB DOWN
        if self._is_thumb_down(landmarks):
            return "THUMB_DOWN"
        
        # PEACE SIGN (Victory/V sign)
        if self._is_peace_sign(landmarks):
            return "PEACE_SIGN"
        
        return None
    
    def _detect_swipe(self, current_position) -> Optional[str]:
        """Detect swipe gestures based on hand movement"""
        if self.prev_hand_position is None:
            self.prev_hand_position = current_position
            return None
        
        # Calculate movement
        delta_x = current_position[0] - self.prev_hand_position[0]
        delta_y = current_position[1] - self.prev_hand_position[1]
        
        threshold = GESTURE_CONFIG["swipe_threshold"]
        
        # Detect horizontal swipe
        if abs(delta_x) > threshold and abs(delta_y) < threshold / 2:
            self.prev_hand_position = current_position
            if delta_x > 0:
                return "SWIPE_RIGHT"
            else:
                return "SWIPE_LEFT"
        
        # Update previous position gradually
        self.prev_hand_position = current_position
        return None
    
    def _all_fingers_extended(self, landmarks) -> bool:
        """Check if all fingers are extended (open palm)"""
        # Check index, middle, ring, pinky
        finger_tips = [8, 12, 16, 20]
        finger_bases = [6, 10, 14, 18]
        
        for tip_idx, base_idx in zip(finger_tips, finger_bases):
            if landmarks[tip_idx][1] >= landmarks[base_idx][1]:  # Tip should be above base
                return False
        
        return True
    
    def _all_fingers_closed(self, landmarks) -> bool:
        """Check if all fingers are closed (fist)"""
        # Check if fingertips are close to palm
        palm_center = landmarks[0]  # Wrist as reference
        finger_tips = [4, 8, 12, 16, 20]
        
        distances = []
        for tip_idx in finger_tips:
            dist = np.linalg.norm(np.array(landmarks[tip_idx][:2]) - np.array(palm_center[:2]))
            distances.append(dist)
        
        # All fingertips should be close to palm
        return all(d < 0.15 for d in distances)
    
    def _is_thumb_up(self, landmarks) -> bool:
        """Check for thumbs up gesture"""
        thumb_tip = landmarks[4]
        thumb_base = landmarks[2]
        index_tip = landmarks[8]
        wrist = landmarks[0]
        
        # Thumb pointing up
        thumb_up = thumb_tip[1] < thumb_base[1] < wrist[1]
        
        # Other fingers closed
        finger_tips = [8, 12, 16, 20]
        fingers_closed = all(landmarks[tip][1] > landmarks[tip-2][1] for tip in finger_tips)
        
        return thumb_up and fingers_closed
    
    def _is_thumb_down(self, landmarks) -> bool:
        """Check for thumbs down gesture"""
        thumb_tip = landmarks[4]
        thumb_base = landmarks[2]
        wrist = landmarks[0]
        
        # Thumb pointing down
        thumb_down = thumb_tip[1] > thumb_base[1] > wrist[1]
        
        # Other fingers closed
        finger_tips = [8, 12, 16, 20]
        fingers_closed = all(landmarks[tip][1] > landmarks[tip-2][1] for tip in finger_tips)
        
        return thumb_down and fingers_closed
    
    def _is_peace_sign(self, landmarks) -> bool:
        """Check for peace/victory sign (index and middle fingers up)"""
        # Index and middle fingers extended
        index_extended = landmarks[8][1] < landmarks[6][1]
        middle_extended = landmarks[12][1] < landmarks[10][1]
        
        # Ring and pinky closed
        ring_closed = landmarks[16][1] >= landmarks[14][1]
        pinky_closed = landmarks[20][1] >= landmarks[18][1]
        
        return index_extended and middle_extended and ring_closed and pinky_closed
    
    def _validate_gesture(self, gesture: str) -> bool:
        """Validate gesture with debouncing and hold time"""
        current_time = time.time()
        
        # Check debounce time
        if (self.last_gesture == gesture and 
            current_time - self.last_gesture_time < GESTURE_CONFIG.get("gesture_hold_time", 0.3)):
            return False
        
        # Add to history
        self.gesture_history.append(gesture)
        if len(self.gesture_history) > self.history_size:
            self.gesture_history.pop(0)
        
        # Check if gesture is consistent
        if len(self.gesture_history) >= 3:
            recent_gestures = self.gesture_history[-3:]
            if recent_gestures.count(gesture) >= 2:
                self.last_gesture = gesture
                self.last_gesture_time = current_time
                return True
        
        return False
    
    def get_fps(self) -> float:
        """Get current FPS"""
        if self.cap:
            return self.cap.get(cv2.CAP_PROP_FPS)
        return 0.0
    
    def is_active(self) -> bool:
        """Check if camera is active"""
        return self.cap is not None and self.cap.isOpened()
