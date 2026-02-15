import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock modules before import
mock_sr = MagicMock()
sys.modules["speech_recognition"] = mock_sr
sys.modules["pyaudio"] = MagicMock()
sys.modules["vosk"] = MagicMock()

# Import module under test
from voice_recognizer import VoiceRecognizer

class TestVoiceOptimization(unittest.TestCase):

    def setUp(self):
        # Reset mocks
        mock_sr.reset_mock()

    def test_listen_loop_single_open(self):
        """Verify that _listen_loop opens microphone only once (optimized)"""
        # Create mock instances to return
        mock_mic_instance = MagicMock()
        mock_rec_instance = MagicMock()

        # Configure the mock module to return these instances
        mock_sr.Microphone.return_value = mock_mic_instance
        mock_sr.Recognizer.return_value = mock_rec_instance

        # Mock the context manager behavior
        mock_source = MagicMock()
        mock_mic_instance.__enter__.return_value = mock_source

        # Instantiate (triggers _calibrate_microphone -> one __enter__)
        vr = VoiceRecognizer()

        # Verify __init__ called __enter__ once
        self.assertEqual(mock_mic_instance.__enter__.call_count, 1)

        # Reset counts to test the loop independently
        mock_mic_instance.__enter__.reset_mock()

        # Control loop: 3 iterations
        # We need to stop the loop, so we patch listen to modify is_listening
        # We also need to mock time.sleep to avoid waiting if exceptions occur
        # But our mock listen won't raise exceptions unless we tell it to.

        call_count = 0
        def listen_side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count >= 3:
                vr.is_listening = False
            return MagicMock() # return dummy audio

        mock_rec_instance.listen.side_effect = listen_side_effect

        # Start loop
        vr.is_listening = True
        vr._listen_loop()

        # Currently, it should be called 1 time (once for the whole loop)
        print(f"DEBUG: Microphone.__enter__ called {mock_mic_instance.__enter__.call_count} times in loop")

        # Assert optimization
        # We expect 1 call because the `with` block is outside the loop
        self.assertEqual(mock_mic_instance.__enter__.call_count, 1)

if __name__ == "__main__":
    unittest.main()
