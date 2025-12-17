"""
Configuration file for Presentation Control Tool
Contains modes, gesture mappings, voice commands, and keyboard shortcuts
"""

import os
import json
from enum import Enum

# Operation Modes
class OperationMode(Enum):
    GESTURE_ONLY = "gesture"
    VOICE_ONLY = "voice"
    HYBRID = "hybrid"

# Default Configuration
DEFAULT_CONFIG = {
    "mode": OperationMode.HYBRID.value,
    "gesture_sensitivity": 0.7,
    "voice_sensitivity": 0.6,
    "debounce_time": 0.5,  # seconds
    "camera_index": 0,
    "show_ui": True,
    "sound_effects": True,
    "offline_mode": False,
    "language": "both"  # "indonesian", "english", or "both"
}

# Gesture Mappings
GESTURE_COMMANDS = {
    "SWIPE_RIGHT": "next",
    "SWIPE_LEFT": "previous",
    "OPEN_PALM": "pause",
    "CLOSED_FIST": "play",
    "THUMB_UP": "first",
    "THUMB_DOWN": "last",
    "PEACE_SIGN": "blackout"
}

# Voice Commands (Indonesian & English)
VOICE_COMMANDS = {
    # Navigation
    "next": ["next", "lanjut", "berikutnya", "selanjutnya"],
    "previous": ["previous", "back", "kembali", "sebelumnya", "mundur"],
    "first": ["first", "start", "pertama", "awal", "mulai"],
    "last": ["last", "end", "terakhir", "akhir"],
    
    # Control
    "pause": ["pause", "stop", "berhenti", "jeda"],
    "play": ["play", "resume", "lanjutkan", "mulai"],
    "blackout": ["black", "blackout", "hitam", "gelap"],
    "exit": ["exit", "quit", "close", "keluar", "tutup"]
}

# Application-specific keyboard shortcuts
APP_PROFILES = {
    "powerpoint": {
        "next": ["right"],
        "previous": ["left"],
        "first": ["home"],
        "last": ["end"],
        "pause": ["b"],
        "play": ["b"],
        "blackout": ["b"],
        "exit": ["esc"],
        "start_presentation": ["f5"]
    },
    "google_slides": {
        "next": ["right", "space"],
        "previous": ["left", "backspace"],
        "first": ["home"],
        "last": ["end"],
        "pause": ["s"],
        "play": ["s"],
        "blackout": ["b"],
        "exit": ["esc"],
        "start_presentation": ["ctrl", "f5"]
    },
    "pdf_viewer": {
        "next": ["right", "pagedown"],
        "previous": ["left", "pageup"],
        "first": ["home"],
        "last": ["end"],
        "pause": [],
        "play": [],
        "blackout": [],
        "exit": ["esc"],
        "start_presentation": ["f5"]
    },
    "canva": {
        "next": ["right"],
        "previous": ["left"],
        "first": ["home"],
        "last": ["end"],
        "pause": [],
        "play": [],
        "blackout": [],
        "exit": ["esc"],
        "start_presentation": []
    },
    "universal": {  # Fallback for unknown apps
        "next": ["right"],
        "previous": ["left"],
        "first": ["home"],
        "last": ["end"],
        "pause": [],
        "play": [],
        "blackout": [],
        "exit": ["esc"],
        "start_presentation": []
    }
}

# Mode switching hotkeys
MODE_HOTKEYS = {
    "g": OperationMode.GESTURE_ONLY,
    "v": OperationMode.VOICE_ONLY,
    "h": OperationMode.HYBRID
}

# Gesture detection parameters
GESTURE_CONFIG = {
    "min_detection_confidence": 0.7,
    "min_tracking_confidence": 0.5,
    "swipe_threshold": 0.15,  # Minimum distance for swipe
    "gesture_hold_time": 0.3,  # Time to hold gesture for confirmation
    "max_hands": 1  # Track only one hand
}

# Voice recognition parameters
VOICE_CONFIG = {
    "energy_threshold": 4000,
    "dynamic_energy": True,
    "pause_threshold": 0.8,
    "phrase_timeout": 2,
    "vosk_model_path": "./models/vosk-model-small-id-0.22"
}

# UI Display settings
UI_CONFIG = {
    "window_name": "Presentation Controller",
    "show_landmarks": True,
    "show_fps": True,
    "show_status": True,
    "overlay_color": (0, 255, 0),  # Green
    "text_color": (255, 255, 255),  # White
    "font_scale": 0.7,
    "font_thickness": 2
}

# Configuration file path
CONFIG_FILE = "user_config.json"


class ConfigManager:
    """Manages user configuration with persistence"""
    
    def __init__(self):
        self.config = DEFAULT_CONFIG.copy()
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()
    
    def get_mode(self):
        """Get current operation mode"""
        mode_str = self.config.get("mode", OperationMode.HYBRID.value)
        return OperationMode(mode_str)
    
    def set_mode(self, mode: OperationMode):
        """Set operation mode"""
        self.set("mode", mode.value)


# Singleton instance
config_manager = ConfigManager()
