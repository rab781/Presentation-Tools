import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock modules before import
mock_cv2 = MagicMock()
sys.modules["cv2"] = mock_cv2
mock_np = MagicMock()
sys.modules["numpy"] = mock_np
mock_pyautogui = MagicMock()
sys.modules["pyautogui"] = mock_pyautogui
mock_pyaudio = MagicMock()
sys.modules["pyaudio"] = mock_pyaudio
mock_sr = MagicMock()
sys.modules["speech_recognition"] = mock_sr
mock_vosk = MagicMock()
sys.modules["vosk"] = mock_vosk

import threading
import queue
import time
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import VoiceRecognizer
try:
    from voice_recognizer import VoiceRecognizer
except ImportError:
    print("Failed to import VoiceRecognizer")
    sys.exit(1)

class TestVoiceOptimization(unittest.TestCase):
    def setUp(self):
        # Reset mocks
        mock_sr.reset_mock()

        # Setup Recognizer and Microphone mocks
        self.mock_recognizer_instance = MagicMock()
        mock_sr.Recognizer.return_value = self.mock_recognizer_instance

        self.mock_microphone_instance = MagicMock()
        mock_sr.Microphone.return_value = self.mock_microphone_instance

        # Microphone context manager setup
        self.mock_microphone_instance.__enter__.return_value = self.mock_microphone_instance
        self.mock_microphone_instance.__exit__.return_value = None

    def test_microphone_reopened_in_loop(self):
        """
        Test to demonstrate that the microphone is currently re-opened in every iteration of the loop.
        """
        recognizer = VoiceRecognizer(offline_mode=False)
        self.mock_microphone_instance.reset_mock() # Reset after init calibration

        # We need to simulate the loop running for a few iterations.
        # We can do this by making recognizer.listen have a side effect.
        # It will be called inside the loop.

        # Iteration 1: success
        # Iteration 2: success
        # Iteration 3: stop loop

        def listen_side_effect(source, timeout=None, phrase_time_limit=None):
            # Check if source is correct
            if source is not self.mock_microphone_instance:
                raise ValueError("Source is not the mock microphone")

            # Decrement a counter or check state to stop loop
            if not hasattr(listen_side_effect, 'counter'):
                listen_side_effect.counter = 0
            listen_side_effect.counter += 1

            if listen_side_effect.counter >= 3:
                recognizer.is_listening = False
                return MagicMock() # Return dummy audio

            return MagicMock() # Return dummy audio

        self.mock_recognizer_instance.listen.side_effect = listen_side_effect

        # Start listening manually (call the loop function directly to avoid threading complexity if possible)
        # However, _listen_loop is designed to run in a thread.
        # But for unit testing, we can just call it synchronously since we mocked the blocking calls.

        recognizer.is_listening = True
        recognizer._listen_loop()

        # Verify call count of __enter__
        # In the inefficient version, it should be called 3 times (once per iteration).
        print(f"Microphone.__enter__ called {self.mock_microphone_instance.__enter__.call_count} times")

        # Assert that it is called exactly ONCE (demonstrating the optimization)
        # The loop ran 3 times, but we only entered the context manager once.
        self.assertEqual(self.mock_microphone_instance.__enter__.call_count, 1,
                        "Microphone context manager should be called exactly once for the entire loop duration")

if __name__ == '__main__':
    unittest.main()
