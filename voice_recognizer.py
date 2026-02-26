"""
Voice Recognition Module
Supports both online (Google) and offline (Vosk) speech recognition
Bilingual support: Indonesian and English
"""

import speech_recognition as sr
import threading
import queue
import time
import os
from typing import Optional, Callable
from config import VOICE_COMMANDS, VOICE_CONFIG


class VoiceRecognizer:
    """Voice command recognition with online and offline support"""
    
    def __init__(self, offline_mode=False):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.offline_mode = offline_mode
        
        # Setup recognizer parameters
        self.recognizer.energy_threshold = VOICE_CONFIG.get("energy_threshold", 4000)
        self.recognizer.dynamic_energy_threshold = VOICE_CONFIG.get("dynamic_energy", True)
        self.recognizer.pause_threshold = VOICE_CONFIG.get("pause_threshold", 0.8)
        
        # Command queue
        self.command_queue = queue.Queue()
        
        # Listening state
        self.is_listening = False
        self.listen_thread = None
        
        # Callback for commands
        self.command_callback: Optional[Callable] = None
        
        # Vosk model (for offline mode)
        self.vosk_model = None
        if offline_mode:
            self._load_vosk_model()
        
        # Calibrate microphone
        self._calibrate_microphone()
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        print("Calibrating microphone for ambient noise...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print(f"Microphone calibrated. Energy threshold: {self.recognizer.energy_threshold}")
        except Exception as e:
            print(f"Warning: Could not calibrate microphone: {e}")
    
    def _load_vosk_model(self):
        """Load Vosk model for offline recognition"""
        try:
            from vosk import Model
            model_path = VOICE_CONFIG.get("vosk_model_path", "./models/vosk-model-small-id-0.22")
            
            if os.path.exists(model_path):
                self.vosk_model = Model(model_path)
                print(f"Vosk model loaded from {model_path}")
            else:
                print(f"Warning: Vosk model not found at {model_path}")
                print("Download from: https://alphacephei.com/vosk/models")
                self.offline_mode = False
        except ImportError:
            print("Warning: Vosk not installed. Install with: pip install vosk")
            self.offline_mode = False
    
    def start_listening(self, callback: Optional[Callable] = None):
        """Start listening for voice commands in background thread"""
        if self.is_listening:
            return
        
        self.command_callback = callback
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        print("Voice recognition started")
    
    def stop_listening(self):
        """Stop listening for voice commands"""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        print("Voice recognition stopped")
    
    def _listen_loop(self):
        """Main listening loop (runs in background thread)"""
        while self.is_listening:
            try:
                # Optimization: Open microphone stream once to reduce overhead
                with self.microphone as source:
                    while self.is_listening:
                        try:
                            # Listen for audio
                            audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)

                            # Recognize speech
                            command = self._recognize_speech(audio)

                            if command:
                                # Map to action
                                action = self._map_command_to_action(command)
                                if action:
                                    # Add to queue
                                    self.command_queue.put(action)

                                    # Call callback if provided
                                    if self.command_callback:
                                        self.command_callback(action)

                                    print(f"Voice command detected: '{command}' -> {action}")
                        
                        except sr.WaitTimeoutError:
                            # No speech detected, continue listening
                            continue
            
            except Exception as e:
                if self.is_listening:
                    print(f"Error in voice recognition: {e}")
                time.sleep(0.1)
    
    def _recognize_speech(self, audio) -> Optional[str]:
        """Recognize speech from audio data"""
        try:
            if self.offline_mode and self.vosk_model:
                # Use Vosk for offline recognition
                return self._recognize_with_vosk(audio)
            else:
                # Use Google Speech Recognition (online)
                return self._recognize_with_google(audio)
        except Exception as e:
            print(f"Recognition error: {e}")
            return None
    
    def _recognize_with_google(self, audio) -> Optional[str]:
        """Recognize speech using Google Speech Recognition"""
        try:
            # Try Indonesian first, then English
            text = None
            try:
                text = self.recognizer.recognize_google(audio, language="id-ID")  # type: ignore
            except:
                try:
                    text = self.recognizer.recognize_google(audio, language="en-US")  # type: ignore
                except:
                    pass
            
            if text:
                return text.lower().strip()
        except sr.UnknownValueError:
            # Speech not understood
            pass
        except sr.RequestError as e:
            print(f"Google API error: {e}")
            # Fallback to offline if available
            if self.vosk_model:
                return self._recognize_with_vosk(audio)
        
        return None
    
    def _recognize_with_vosk(self, audio) -> Optional[str]:
        """Recognize speech using Vosk (offline)"""
        try:
            from vosk import KaldiRecognizer
            import json
            
            # Convert audio to proper format
            raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
            
            # Create recognizer
            rec = KaldiRecognizer(self.vosk_model, 16000)
            
            # Process audio
            if rec.AcceptWaveform(raw_data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    return text.lower().strip()
            
            # Try partial result
            partial = json.loads(rec.PartialResult())
            text = partial.get("partial", "")
            if text:
                return text.lower().strip()
        
        except Exception as e:
            print(f"Vosk recognition error: {e}")
        
        return None
    
    def _map_command_to_action(self, text: str) -> Optional[str]:
        """Map recognized text to action command"""
        if not text:
            return None
        
        text = text.lower().strip()
        
        # Check each command category
        for action, keywords in VOICE_COMMANDS.items():
            for keyword in keywords:
                if keyword in text:
                    return action
        
        return None
    
    def get_command(self, timeout: float = 0.1) -> Optional[str]:
        """Get command from queue (non-blocking)"""
        try:
            return self.command_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def has_commands(self) -> bool:
        """Check if there are pending commands"""
        return not self.command_queue.empty()
    
    def clear_commands(self):
        """Clear all pending commands"""
        while not self.command_queue.empty():
            try:
                self.command_queue.get_nowait()
            except queue.Empty:
                break
    
    def test_microphone(self) -> bool:
        """Test if microphone is working"""
        try:
            with self.microphone as source:
                print("Testing microphone... Say something!")
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=3)
                text = self._recognize_speech(audio)
                
                if text:
                    print(f"Microphone test successful! Heard: '{text}'")
                    return True
                else:
                    print("Microphone test: No speech detected")
                    return False
        except Exception as e:
            print(f"Microphone test failed: {e}")
            return False
    
    def is_active(self) -> bool:
        """Check if voice recognition is active"""
        return self.is_listening
    
    def get_status(self) -> dict:
        """Get current status"""
        return {
            "active": self.is_listening,
            "mode": "offline" if self.offline_mode else "online",
            "energy_threshold": self.recognizer.energy_threshold,
            "pending_commands": self.command_queue.qsize()
        }
