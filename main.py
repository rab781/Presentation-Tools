"""
Presentation Control Tool
Main application for controlling presentations using hand gestures and voice commands
Author: GitHub Copilot
Date: December 17, 2025
"""

import cv2
import numpy as np
import time
import sys
import threading
from typing import Optional

# Import custom modules
from gesture_detector import GestureDetector
from voice_recognizer import VoiceRecognizer
from controller import PresentationController, CalibrationWizard
from config import (
    OperationMode, 
    config_manager, 
    MODE_HOTKEYS, 
    UI_CONFIG
)


class PresentationToolApp:
    """Main application class"""
    
    def __init__(self):
        # Load configuration
        self.config = config_manager
        self.mode = self.config.get_mode()
        
        # Initialize components
        self.gesture_detector: Optional[GestureDetector] = None
        self.voice_recognizer: Optional[VoiceRecognizer] = None
        debounce = self.config.get("debounce_time", 0.5)
        self.controller = PresentationController(
            debounce_time=debounce if debounce is not None else 0.5
        )
        
        # UI state
        self.show_ui = self.config.get("show_ui", True)
        self.running = False
        self.paused = False
        
        # FPS tracking
        self.fps_start_time = time.time()
        self.fps_frame_count = 0
        self.fps = 0
        
        # Status message
        self.status_message = "Initializing..."
        self.last_command = ""
        self.command_source = ""
    
    def initialize(self):
        """Initialize all components"""
        print("\n" + "="*60)
        print("PRESENTATION CONTROL TOOL")
        print("="*60)
        print(f"Mode: {self.mode.value.upper()}")
        print()
        
        # Initialize gesture detector
        if self.mode in [OperationMode.GESTURE_ONLY, OperationMode.HYBRID]:
            try:
                cam_idx = self.config.get("camera_index", 0)
                self.gesture_detector = GestureDetector(
                    camera_index=cam_idx if cam_idx is not None else 0
                )
                self.gesture_detector.start()
                print("✓ Gesture detection initialized")
            except Exception as e:
                print(f"✗ Failed to initialize gesture detection: {e}")
                if self.mode == OperationMode.GESTURE_ONLY:
                    print("Switching to voice-only mode")
                    self.mode = OperationMode.VOICE_ONLY
        
        # Initialize voice recognizer
        if self.mode in [OperationMode.VOICE_ONLY, OperationMode.HYBRID]:
            try:
                offline = self.config.get("offline_mode", False)
                self.voice_recognizer = VoiceRecognizer(
                    offline_mode=offline if offline is not None else False
                )
                self.voice_recognizer.start_listening(
                    callback=self._on_voice_command
                )
                print("✓ Voice recognition initialized")
            except Exception as e:
                print(f"✗ Failed to initialize voice recognition: {e}")
                if self.mode == OperationMode.VOICE_ONLY:
                    print("Switching to gesture-only mode")
                    self.mode = OperationMode.GESTURE_ONLY
        
        # Start controller
        self.controller.start()
        self.controller.auto_detect_application()
        print("✓ Controller initialized")
        
        print("\n" + "-"*60)
        print("CONTROLS:")
        print("  G - Gesture Only mode")
        print("  V - Voice Only mode")
        print("  H - Hybrid mode (both)")
        print("  C - Run calibration")
        print("  A - Auto-detect application")
        print("  S - Select application manually")
        print("  P - Pause/Resume")
        print("  ESC - Exit")
        print("-"*60)
        print()
        
        self.status_message = "Ready"
    
    def _on_voice_command(self, command: str):
        """Callback for voice commands"""
        self.last_command = command
        self.command_source = "voice"
        self.controller.send_command(command, source="voice")
    
    def _process_gesture(self, gesture_command: str):
        """Process gesture command"""
        if gesture_command:
            self.last_command = gesture_command
            self.command_source = "gesture"
            self.controller.send_command(gesture_command, source="gesture")
    
    def _select_application(self):
        """Let user manually select application profile"""
        print("\n" + "="*60)
        print("SELECT APPLICATION PROFILE")
        print("="*60)
        print("1. PowerPoint")
        print("2. Google Slides")
        print("3. PDF Viewer")
        print("4. Canva")
        print("5. Universal (works with any app)")
        print("A. Auto-detect")
        print("="*60)
        print("Press number key (1-5) or A...")
    
    def _update_fps(self):
        """Update FPS counter"""
        self.fps_frame_count += 1
        elapsed = time.time() - self.fps_start_time
        
        if elapsed > 1.0:
            self.fps = self.fps_frame_count / elapsed
            self.fps_frame_count = 0
            self.fps_start_time = time.time()
    
    def _draw_ui(self, frame: np.ndarray) -> np.ndarray:
        """Draw UI overlay on frame"""
        if not self.show_ui:
            return frame
        
        h, w = frame.shape[:2]
        
        # ⚡ OPTIMIZATION: Instead of copying the entire frame and blending
        # the whole image, we only extract the Region of Interest (ROI) for
        # the top banner (120 pixels) and blend just that section.
        # This prevents an expensive memory allocation (frame.copy()) and
        # reduces the area processed by cv2.addWeighted, saving CPU cycles and
        # reducing garbage collection overhead per frame.
        # Expected Impact: Eliminates one full frame allocation and reduces blending computations by ~75% (for 480p).
        roi = frame[0:120, 0:w]
        # ⚡ OPTIMIZATION: In-place alpha blending
        # By passing `dst=roi` to cv2.addWeighted, we perform the blending operation
        # directly in the memory of the original frame's slice if possible, avoiding
        # an intermediate array allocation. We assign the result back to the frame slice
        # to ensure the UI updates correctly even if OpenCV falls back to out-of-place execution.
        frame[0:120, 0:w] = cv2.addWeighted(roi, 0.4, roi, 0, 0, dst=roi)
        
        # Title
        cv2.putText(frame, "Presentation Controller", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, UI_CONFIG["text_color"], 2)
        
        # Mode
        mode_text = f"Mode: {self.mode.value.upper()}"
        mode_color = (0, 255, 0) if not self.paused else (0, 165, 255)
        if self.paused:
            mode_text += " (PAUSED)"
        cv2.putText(frame, mode_text, (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, mode_color, 2)
        
        # Status
        status_text = f"Status: {self.status_message}"
        cv2.putText(frame, status_text, (10, 85),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, UI_CONFIG["text_color"], 1)
        
        # Last command
        if self.last_command:
            cmd_text = f"Last: {self.last_command} ({self.command_source})"
            cv2.putText(frame, cmd_text, (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        # FPS
        if UI_CONFIG.get("show_fps", True):
            fps_text = f"FPS: {self.fps:.1f}"
            cv2.putText(frame, fps_text, (w - 120, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, UI_CONFIG["text_color"], 2)
        
        # Application
        app_text = f"App: {self.controller.current_app}"
        cv2.putText(frame, app_text, (w - 200, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, UI_CONFIG["text_color"], 1)
        
        return frame
    
    def _switch_mode(self, new_mode: OperationMode):
        """Switch operation mode"""
        if new_mode == self.mode:
            return
        
        print(f"\nSwitching to {new_mode.value.upper()} mode")
        
        # Stop current components
        if self.gesture_detector and new_mode == OperationMode.VOICE_ONLY:
            self.gesture_detector.stop()
            self.gesture_detector = None
        
        if self.voice_recognizer and new_mode == OperationMode.GESTURE_ONLY:
            self.voice_recognizer.stop_listening()
            self.voice_recognizer = None
        
        # Start new components
        if not self.gesture_detector and new_mode in [OperationMode.GESTURE_ONLY, OperationMode.HYBRID]:
            try:
                self.gesture_detector = GestureDetector()
                self.gesture_detector.start()
                print("✓ Gesture detection activated")
            except Exception as e:
                print(f"✗ Failed to activate gesture detection: {e}")
        
        if not self.voice_recognizer and new_mode in [OperationMode.VOICE_ONLY, OperationMode.HYBRID]:
            try:
                self.voice_recognizer = VoiceRecognizer()
                self.voice_recognizer.start_listening(callback=self._on_voice_command)
                print("✓ Voice recognition activated")
            except Exception as e:
                print(f"✗ Failed to activate voice recognition: {e}")
        
        self.mode = new_mode
        self.config.set_mode(new_mode)
        self.status_message = f"Mode: {new_mode.value}"
    
    def run(self):
        """Main application loop"""
        self.running = True
        self.status_message = "Running"
        
        try:
            while self.running:
                # Process gesture if enabled
                if self.gesture_detector and not self.paused:
                    success, frame = self.gesture_detector.read_frame()
                    
                    if success and frame is not None:
                        # Detect gesture
                        gesture_command, annotated_frame = self.gesture_detector.detect_gesture(
                            frame, 
                            draw_landmarks=UI_CONFIG.get("show_landmarks", True)
                        )
                        
                        # Process gesture command
                        if gesture_command:
                            self._process_gesture(gesture_command)
                        
                        # Draw UI
                        if self.show_ui:
                            display_frame = self._draw_ui(annotated_frame)
                            cv2.imshow(UI_CONFIG["window_name"], display_frame)
                        
                        # Update FPS
                        self._update_fps()
                else:
                    # Voice-only mode or paused - just show status window
                    if self.show_ui:
                        # Create blank frame with status
                        status_frame = np.zeros((200, 640, 3), dtype=np.uint8)
                        status_frame = self._draw_ui(status_frame)
                        cv2.imshow(UI_CONFIG["window_name"], status_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == 27:  # ESC
                    print("\nExiting...")
                    self.running = False
                elif key == ord('g') or key == ord('G'):
                    self._switch_mode(OperationMode.GESTURE_ONLY)
                elif key == ord('v') or key == ord('V'):
                    self._switch_mode(OperationMode.VOICE_ONLY)
                elif key == ord('h') or key == ord('H'):
                    self._switch_mode(OperationMode.HYBRID)
                elif key == ord('p') or key == ord('P'):
                    self.paused = not self.paused
                    self.status_message = "Paused" if self.paused else "Running"
                    print(f"\n{'Paused' if self.paused else 'Resumed'}")
                elif key == ord('c') or key == ord('C'):
                    print("\nRunning calibration...")
                    CalibrationWizard.run_calibration()
                elif key == ord('a') or key == ord('A'):
                    print("\nAuto-detecting application...")
                    self.controller.auto_detect_application()
                elif key == ord('s') or key == ord('S'):
                    self._select_application()
                elif key == ord('1'):
                    self.controller.set_application("powerpoint")
                    print("\nSet to PowerPoint mode")
                elif key == ord('2'):
                    self.controller.set_application("google_slides")
                    print("\nSet to Google Slides mode")
                elif key == ord('3'):
                    self.controller.set_application("pdf_viewer")
                    print("\nSet to PDF Viewer mode")
                elif key == ord('4'):
                    self.controller.set_application("canva")
                    print("\nSet to Canva mode")
                elif key == ord('5'):
                    self.controller.set_application("universal")
                    print("\nSet to Universal mode")
                
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        except Exception as e:
            print(f"\nError in main loop: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        print("\nCleaning up...")
        
        if self.gesture_detector:
            self.gesture_detector.stop()
        
        if self.voice_recognizer:
            self.voice_recognizer.stop_listening()
        
        self.controller.stop()
        
        cv2.destroyAllWindows()
        
        print("Cleanup complete")


def main():
    """Main entry point"""
    print("\nPresentation Control Tool")
    print("Starting...")
    
    # Check if user wants calibration
    if len(sys.argv) > 1 and sys.argv[1] in ['--calibrate', '-c']:
        CalibrationWizard.run_calibration()
        return
    
    # Create and run app
    app = PresentationToolApp()
    app.initialize()
    app.run()


if __name__ == "__main__":
    main()

