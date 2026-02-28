import sys
import unittest
from unittest.mock import MagicMock, patch
import os
import time

# Mock modules before import
mock_sr = MagicMock()
sys.modules["speech_recognition"] = mock_sr

class WaitTimeoutError(Exception):
    pass
mock_sr.WaitTimeoutError = WaitTimeoutError

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from voice_recognizer import VoiceRecognizer
except ImportError:
    print("Could not import voice_recognizer. Dependencies might be missing even with mocks.")
    sys.exit(1)

class TestVoiceOptimization(unittest.TestCase):
    def setUp(self):
        mock_sr.reset_mock()

    @patch('voice_recognizer.VoiceRecognizer._calibrate_microphone')
    def test_listen_loop_single_context_entry(self, mock_calibrate):
        # We want to test that the loop stays inside the `with self.microphone` block
        # when WaitTimeoutError is raised

        recognizer = VoiceRecognizer()

        # Mock microphone context manager
        mock_mic = MagicMock()
        mock_enter = MagicMock()
        mock_exit = MagicMock()
        mock_mic.__enter__ = mock_enter
        mock_mic.__exit__ = mock_exit
        recognizer.microphone = mock_mic

        # We need to simulate the inner loop running multiple times and then exiting.
        # We'll make recognizer.listen raise WaitTimeoutError twice, and then we'll
        # set is_listening = False to break the loop on the third time.

        call_count = [0]

        def mock_listen(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] <= 2:
                raise mock_sr.WaitTimeoutError()
            else:
                recognizer.is_listening = False
                raise Exception("Stop the loop")

        recognizer.recognizer.listen.side_effect = mock_listen

        # Set is_listening to True so the loop runs
        recognizer.is_listening = True

        # Run the loop (it should run in the current thread since we are calling it directly)
        recognizer._listen_loop()

        # The microphone context manager should only be entered ONCE,
        # despite `listen` being called multiple times and raising WaitTimeoutError
        mock_enter.assert_called_once()

        # listen should have been called 3 times
        self.assertEqual(recognizer.recognizer.listen.call_count, 3)

    @patch('voice_recognizer.VoiceRecognizer._calibrate_microphone')
    def test_listen_loop_reinitializes_on_error(self, mock_calibrate):
        # Test that the microphone stream is correctly re-initialized (new context entry) upon critical errors.
        recognizer = VoiceRecognizer()

        mock_mic = MagicMock()
        mock_enter = MagicMock()
        mock_exit = MagicMock()
        mock_mic.__enter__ = mock_enter
        mock_mic.__exit__ = mock_exit
        recognizer.microphone = mock_mic

        call_count = [0]

        def mock_listen(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                # First time: raise generic exception to break inner loop
                raise Exception("Critical error")
            elif call_count[0] == 2:
                # Second time: stop the loop
                recognizer.is_listening = False
                raise Exception("Stop the loop")

        recognizer.recognizer.listen.side_effect = mock_listen

        recognizer.is_listening = True

        recognizer._listen_loop()

        # The microphone context manager should have been entered TWICE,
        # because the generic exception causes the inner loop to break,
        # and the outer loop re-enters the context manager.
        self.assertEqual(mock_enter.call_count, 2)
        self.assertEqual(recognizer.recognizer.listen.call_count, 2)

if __name__ == '__main__':
    unittest.main()
