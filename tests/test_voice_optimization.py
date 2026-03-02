import sys
import unittest
from unittest.mock import MagicMock, patch
import os

# Mock modules before import
mock_sr = MagicMock()
sys.modules["speech_recognition"] = mock_sr

class MockWaitTimeoutError(Exception):
    pass
mock_sr.WaitTimeoutError = MockWaitTimeoutError

class MockMicrophoneContextManager:
    def __init__(self):
        self.enter_calls = 0
    def __enter__(self):
        self.enter_calls += 1
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

mock_mic = MockMicrophoneContextManager()
mock_sr.Microphone.return_value = mock_mic

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from voice_recognizer import VoiceRecognizer
except ImportError:
    print("Could not import voice_recognizer.")
    sys.exit(1)

class TestVoiceOptimization(unittest.TestCase):
    def setUp(self):
        mock_mic.enter_calls = 0

    @patch.object(VoiceRecognizer, '_calibrate_microphone')
    def test_microphone_context_manager(self, mock_calibrate):
        recognizer = VoiceRecognizer(offline_mode=False)

        call_count = [0]

        def mock_listen(source, timeout=1, phrase_time_limit=3):
            call_count[0] += 1
            if call_count[0] < 5:
                raise mock_sr.WaitTimeoutError()
            else:
                recognizer.is_listening = False
                return MagicMock()

        recognizer.recognizer.listen = mock_listen
        recognizer.is_listening = True

        # This will run the loop 5 times
        recognizer._listen_loop()

        # We assert that the listen function was called 5 times
        self.assertEqual(call_count[0], 5)

        # In the unoptimized code, __enter__ will be called 5 times
        # Our target optimization: __enter__ should be called 1 time!
        self.assertEqual(mock_mic.enter_calls, 1, "Microphone context should only be entered once for timeouts")

    @patch.object(VoiceRecognizer, '_calibrate_microphone')
    def test_microphone_context_manager_error_recovery(self, mock_calibrate):
        recognizer = VoiceRecognizer(offline_mode=False)

        call_count = [0]

        def mock_listen(source, timeout=1, phrase_time_limit=3):
            call_count[0] += 1
            if call_count[0] == 2:
                # Trigger a critical error on the second call
                raise Exception("Critical error")
            elif call_count[0] < 5:
                # Timeouts for the rest
                raise mock_sr.WaitTimeoutError()
            else:
                recognizer.is_listening = False
                return MagicMock()

        recognizer.recognizer.listen = mock_listen
        recognizer.is_listening = True

        # This will run the loop
        recognizer._listen_loop()

        # We assert that the listen function was called 5 times
        self.assertEqual(call_count[0], 5)

        # The context should be entered twice: once initially, and once after the critical error
        self.assertEqual(mock_mic.enter_calls, 2, "Microphone context should be re-entered after a critical error")

if __name__ == '__main__':
    unittest.main()
