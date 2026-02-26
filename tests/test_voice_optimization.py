import unittest
from unittest.mock import MagicMock, patch
import sys
import threading
import time

# 1. Mock speech_recognition BEFORE importing voice_recognizer
mock_sr = MagicMock()
class WaitTimeoutError(Exception):
    pass
mock_sr.WaitTimeoutError = WaitTimeoutError
sys.modules["speech_recognition"] = mock_sr

# Ensure voice_recognizer is re-imported if it was already loaded
if "voice_recognizer" in sys.modules:
    del sys.modules["voice_recognizer"]

from voice_recognizer import VoiceRecognizer

class TestVoiceOptimization(unittest.TestCase):
    def setUp(self):
        # Reset mocks
        mock_sr.reset_mock()

        # Setup Microphone mock
        self.mock_microphone_instance = MagicMock()
        # Make it a context manager
        self.mock_microphone_instance.__enter__.return_value = self.mock_microphone_instance
        self.mock_microphone_instance.__exit__.return_value = None
        mock_sr.Microphone.return_value = self.mock_microphone_instance

        # Setup Recognizer mock
        self.mock_recognizer_instance = MagicMock()
        mock_sr.Recognizer.return_value = self.mock_recognizer_instance

    def test_listen_loop_optimized(self):
        """
        Tests that the optimized implementation enters/exits the microphone context
        only once, even when multiple timeouts occur.
        """
        # Patch _calibrate_microphone so it doesn't add to the call count
        with patch.object(VoiceRecognizer, '_calibrate_microphone'):
            vr = VoiceRecognizer(offline_mode=False)

        vr.is_listening = True

        # Counter for loop iterations
        loop_count = 0
        max_loops = 3

        def listen_side_effect(*args, **kwargs):
            nonlocal loop_count
            loop_count += 1
            if loop_count >= max_loops:
                vr.is_listening = False
            # Simulate timeout (silence)
            raise mock_sr.WaitTimeoutError()

        self.mock_recognizer_instance.listen.side_effect = listen_side_effect

        # Run the loop
        vr._listen_loop()

        # Verify call count
        # In optimized code: 1 enter/exit for the entire session.
        print(f"Microphone.__enter__ called {self.mock_microphone_instance.__enter__.call_count} times")

        # We expect exactly 1 call
        self.assertEqual(self.mock_microphone_instance.__enter__.call_count, 1)

if __name__ == '__main__':
    unittest.main()
