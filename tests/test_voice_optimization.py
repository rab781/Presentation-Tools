import unittest
import sys
from unittest.mock import MagicMock, patch
import time
import threading

# Mock speech_recognition before importing voice_recognizer
mock_sr = MagicMock()
sys.modules['speech_recognition'] = mock_sr

# Mock the Microphone class context manager
mock_mic_instance = MagicMock()
mock_mic_instance.__enter__ = MagicMock(return_value=mock_mic_instance)
mock_mic_instance.__exit__ = MagicMock(return_value=None)
mock_sr.Microphone = MagicMock(return_value=mock_mic_instance)

# Mock Recognizer
mock_recognizer_instance = MagicMock()
mock_sr.Recognizer = MagicMock(return_value=mock_recognizer_instance)
mock_sr.WaitTimeoutError = type('WaitTimeoutError', (Exception,), {})

# Now import the module under test
import voice_recognizer

class TestVoiceOptimization(unittest.TestCase):
    def setUp(self):
        # Reset mocks
        mock_mic_instance.__enter__.reset_mock()
        mock_mic_instance.__exit__.reset_mock()
        mock_recognizer_instance.listen.reset_mock()

    def test_microphone_enter_called_once_in_loop(self):
        # Setup the recognizer
        vr = voice_recognizer.VoiceRecognizer(offline_mode=False)

        # Reset mocks after initialization (which might use microphone for calibration)
        mock_mic_instance.__enter__.reset_mock()
        mock_mic_instance.__exit__.reset_mock()
        mock_recognizer_instance.listen.reset_mock()

        # Configure listen to raise WaitTimeoutError a few times, then stop listening
        # We need to stop the loop after a few iterations.
        # VR loop condition is `while self.is_listening`.
        # We can make `listen` side_effect change `is_listening` to False after N calls.

        def listen_side_effect(*args, **kwargs):
            if mock_recognizer_instance.listen.call_count >= 3:
                vr.is_listening = False
            raise mock_sr.WaitTimeoutError()

        mock_recognizer_instance.listen.side_effect = listen_side_effect

        # Start listening (this runs in a thread)
        vr.start_listening()

        # Wait for the thread to finish (it should finish because we set is_listening=False)
        vr.listen_thread.join(timeout=2)

        # Verify loop ran multiple times
        self.assertGreaterEqual(mock_recognizer_instance.listen.call_count, 3,
                                "listen should have been called at least 3 times")

        # KEY ASSERTION:
        # In the unoptimized code, __enter__ is called on every iteration (so >= 3 times).
        # In the optimized code, __enter__ is called exactly ONCE.
        print(f"Microphone.__enter__ called {mock_mic_instance.__enter__.call_count} times")

        # To confirm the current inefficient behavior, we expect this to be > 1.
        # But since I want to use this test to verify the fix later, I will assert == 1.
        # This means the test will FAIL now, and PASS after I fix the code.
        self.assertEqual(mock_mic_instance.__enter__.call_count, 1,
                         "Microphone context manager should only be entered once")

if __name__ == '__main__':
    unittest.main()
