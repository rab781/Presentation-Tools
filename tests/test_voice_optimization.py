import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock modules
mock_sr = MagicMock()
sys.modules["speech_recognition"] = mock_sr

class WaitTimeoutError(Exception):
    pass
mock_sr.WaitTimeoutError = WaitTimeoutError
mock_sr.UnknownValueError = Exception
mock_sr.RequestError = Exception

mock_microphone_instance = MagicMock()
mock_microphone_instance.__enter__ = MagicMock(return_value=mock_microphone_instance)
mock_microphone_instance.__exit__ = MagicMock(return_value=None)
mock_sr.Microphone.return_value = mock_microphone_instance

mock_recognizer_instance = MagicMock()
mock_sr.Recognizer.return_value = mock_recognizer_instance

try:
    from voice_recognizer import VoiceRecognizer
except ImportError as e:
    print(f"Error importing VoiceRecognizer: {e}")
    sys.exit(1)

class TestVoiceOptimization(unittest.TestCase):
    @patch('voice_recognizer.VoiceRecognizer._calibrate_microphone')
    def test_microphone_context_optimization(self, mock_calibrate):
        """
        Test that the microphone context is entered only once across multiple listen attempts (timeouts).
        """
        recognizer = VoiceRecognizer(offline_mode=False)
        recognizer.is_listening = True

        # Simulate 3 timeouts then a stop signal
        def side_effect(*args, **kwargs):
            if mock_recognizer_instance.listen.call_count <= 3:
                raise WaitTimeoutError()
            else:
                recognizer.is_listening = False
                raise Exception("Stop Loop")

        mock_recognizer_instance.listen.side_effect = side_effect

        # Run loop
        with patch('time.sleep'): # Prevent sleep delay
            recognizer._listen_loop()

        # Check call count
        print(f"Microphone.__enter__ called {mock_microphone_instance.__enter__.call_count} times")

        # This assertion will FAIL on unoptimized code (expect > 1 calls)
        # and PASS on optimized code (expect 1 call)
        self.assertEqual(mock_microphone_instance.__enter__.call_count, 1,
                        f"Microphone context should be entered exactly once, but was entered {mock_microphone_instance.__enter__.call_count} times.")

if __name__ == '__main__':
    unittest.main()
