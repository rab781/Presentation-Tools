"""
Presentation Controller Module
Handles keyboard simulation and application-specific commands
"""

import pyautogui
import time
import threading
import queue
from typing import Optional, Dict
from config import APP_PROFILES


# Disable PyAutoGUI failsafe for better UX
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1  # Small pause between actions


class PresentationController:
    """Controls presentation software via keyboard simulation"""
    
    def __init__(self, debounce_time=0.5):
        self.debounce_time = debounce_time
        self.last_command_time = {}
        self.command_queue = queue.Queue()
        
        # Controller state
        self.is_running = False
        self.controller_thread = None
        
        # Current application profile
        self.current_app = "universal"
        self.app_profiles = APP_PROFILES
        
        # Command priority (gesture vs voice)
        self.priority_mode = "hybrid"  # "gesture", "voice", "hybrid"
        
        # Sound effects (optional)
        self.sound_enabled = True
        
    def start(self):
        """Start controller thread"""
        if self.is_running:
            return
        
        self.is_running = True
        self.controller_thread = threading.Thread(target=self._controller_loop, daemon=True)
        self.controller_thread.start()
        print("Presentation controller started")
    
    def stop(self):
        """Stop controller thread"""
        self.is_running = False
        if self.controller_thread:
            self.controller_thread.join(timeout=2)
        print("Presentation controller stopped")
    
    def _controller_loop(self):
        """Main controller loop (runs in background thread)"""
        while self.is_running:
            try:
                # Get command from queue
                command_data = self.command_queue.get(timeout=0.1)
                
                if command_data:
                    command = command_data.get("command")
                    source = command_data.get("source", "unknown")
                    
                    # Execute command
                    if self._should_execute(command):
                        self._execute_command(command, source)
            
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Controller error: {e}")
    
    def send_command(self, command: str, source: str = "manual"):
        """Add command to execution queue"""
        if not command:
            return
        
        self.command_queue.put({
            "command": command,
            "source": source,
            "timestamp": time.time()
        })
    
    def _should_execute(self, command: str) -> bool:
        """Check if command should be executed (debouncing)"""
        current_time = time.time()
        last_time = self.last_command_time.get(command, 0)
        
        if current_time - last_time < self.debounce_time:
            return False
        
        self.last_command_time[command] = current_time
        return True
    
    def _execute_command(self, command: str, source: str):
        """Execute keyboard command based on current app profile"""
        try:
            # Get keyboard shortcuts for current app
            profile = self.app_profiles.get(self.current_app, self.app_profiles["universal"])
            shortcuts = profile.get(command, [])
            
            if not shortcuts:
                print(f"No shortcut defined for '{command}' in {self.current_app} profile")
                return
            
            # Execute keyboard shortcut
            if len(shortcuts) == 1:
                # Single key
                pyautogui.press(shortcuts[0])
            else:
                # Key combination
                pyautogui.hotkey(*shortcuts)
            
            print(f"Executed: {command} ({source}) -> {shortcuts}")
            
            # Play sound effect if enabled
            if self.sound_enabled:
                self._play_sound_effect(command)
        
        except Exception as e:
            print(f"Error executing command '{command}': {e}")
    
    def _play_sound_effect(self, command: str):
        """Play sound effect for command (optional)"""
        # Simple beep using system
        # Can be replaced with actual sound files
        try:
            import winsound
            frequency = 1000  # Hz
            duration = 100    # ms
            
            # Different tones for different commands
            if command in ["next", "previous"]:
                frequency = 800
            elif command in ["first", "last"]:
                frequency = 1200
            elif command == "pause":
                frequency = 600
            
            winsound.Beep(frequency, duration)
        except Exception:
            pass  # Sound not critical
    
    def detect_active_application(self) -> str:
        """Detect currently active presentation application"""
        try:
            import win32gui  # type: ignore
            import win32process
            import psutil
            
            # Get active window
            window = win32gui.GetForegroundWindow()
            if window == 0:
                print("No active window detected")
                return "universal"
            
            # Get window title
            window_title = win32gui.GetWindowText(window).lower()
            
            # Get process name
            try:
                _, process_id = win32process.GetWindowThreadProcessId(window)
                process = psutil.Process(process_id)
                process_name = process.name().lower()
            except Exception:
                process_name = ""
            
            print(f"Active window: '{window_title}'")
            print(f"Process: '{process_name}'")
            
            # Match to known applications by process name first (more reliable)
            if "powerpnt.exe" in process_name or "powerpnt" in process_name:
                detected = "powerpoint"
            elif "chrome.exe" in process_name or "msedge.exe" in process_name or "firefox.exe" in process_name:
                # Browser - check title for specific apps
                if "google slides" in window_title or "presentation" in window_title:
                    detected = "google_slides"
                elif "canva" in window_title:
                    detected = "canva"
                else:
                    detected = "universal"
            elif "acrord" in process_name or "acrobat" in process_name or "foxitreader" in process_name:
                detected = "pdf_viewer"
            # Fallback to window title matching
            elif "powerpoint" in window_title or "pptx" in window_title or ".ppt" in window_title:
                detected = "powerpoint"
            elif "google slides" in window_title:
                detected = "google_slides"
            elif "pdf" in window_title or "adobe" in window_title:
                detected = "pdf_viewer"
            elif "canva" in window_title:
                detected = "canva"
            else:
                detected = "universal"
            
            print(f"Detected application profile: {detected}")
            return detected
        
        except ImportError as e:
            print(f"Warning: Required module not installed ({e}). Using universal profile.")
            print("Install with: pip install psutil pywin32")
            return "universal"
        except Exception as e:
            print(f"Error detecting application: {e}")
            return "universal"
    
    def set_application(self, app_name: str):
        """Manually set active application profile"""
        if app_name in self.app_profiles:
            self.current_app = app_name
            print(f"Application profile set to: {app_name}")
        else:
            print(f"Unknown application: {app_name}. Using universal profile.")
            self.current_app = "universal"
    
    def auto_detect_application(self):
        """Automatically detect and set application profile"""
        detected_app = self.detect_active_application()
        if detected_app != self.current_app:
            self.current_app = detected_app
            print(f"Application detected: {detected_app}")
    
    def get_available_commands(self) -> list:
        """Get list of available commands for current app"""
        profile = self.app_profiles.get(self.current_app, self.app_profiles["universal"])
        return [cmd for cmd, shortcuts in profile.items() if shortcuts]
    
    def test_command(self, command: str):
        """Test a specific command"""
        print(f"Testing command: {command}")
        self._execute_command(command, "test")
    
    def clear_queue(self):
        """Clear command queue"""
        while not self.command_queue.empty():
            try:
                self.command_queue.get_nowait()
            except queue.Empty:
                break
    
    def get_status(self) -> dict:
        """Get controller status"""
        return {
            "active": self.is_running,
            "current_app": self.current_app,
            "pending_commands": self.command_queue.qsize(),
            "available_commands": self.get_available_commands()
        }
    
    # Convenience methods for direct control
    def next_slide(self):
        """Go to next slide"""
        self.send_command("next", "direct")
    
    def previous_slide(self):
        """Go to previous slide"""
        self.send_command("previous", "direct")
    
    def first_slide(self):
        """Go to first slide"""
        self.send_command("first", "direct")
    
    def last_slide(self):
        """Go to last slide"""
        self.send_command("last", "direct")
    
    def pause_presentation(self):
        """Pause/blackout presentation"""
        self.send_command("pause", "direct")
    
    def start_presentation(self):
        """Start presentation mode"""
        self.send_command("start_presentation", "direct")
    
    def exit_presentation(self):
        """Exit presentation mode"""
        self.send_command("exit", "direct")


class CalibrationWizard:
    """Helps user calibrate the system"""
    
    @staticmethod
    def run_calibration():
        """Run calibration wizard"""
        print("\n" + "="*50)
        print("CALIBRATION WIZARD")
        print("="*50)
        
        # Test camera
        print("\n1. Testing camera...")
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    print("✓ Camera working!")
                    height, width = frame.shape[:2]
                    print(f"  Resolution: {width}x{height}")
                else:
                    print("✗ Camera not capturing frames")
                cap.release()
            else:
                print("✗ Cannot open camera")
        except Exception as e:
            print(f"✗ Camera error: {e}")
        
        # Test microphone
        print("\n2. Testing microphone...")
        print("   (This will take a few seconds)")
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print(f"✓ Microphone working!")
                print(f"  Energy threshold: {r.energy_threshold}")
        except Exception as e:
            print(f"✗ Microphone error: {e}")
        
        # Test keyboard control
        print("\n3. Testing keyboard control...")
        try:
            import pyautogui
            print("✓ PyAutoGUI ready!")
            print(f"  Screen size: {pyautogui.size()}")
        except Exception as e:
            print(f"✗ Keyboard control error: {e}")
        
        # Application detection
        print("\n4. Detecting active application...")
        controller = PresentationController()
        app = controller.detect_active_application()
        print(f"✓ Detected: {app}")
        
        print("\n" + "="*50)
        print("CALIBRATION COMPLETE")
        print("="*50)
        print("\nRecommendations:")
        print("- Ensure good lighting for gesture detection")
        print("- Position camera 0.5-2 meters from your hand")
        print("- Reduce background noise for voice recognition")
        print("- Test gestures before starting presentation")
        print()
