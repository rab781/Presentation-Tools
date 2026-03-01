import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Mock modules
mock_sr = MagicMock()
class WaitTimeoutError(Exception):
    pass
mock_sr.WaitTimeoutError = WaitTimeoutError
sys.modules['speech_recognition'] = mock_sr
sys.modules['vosk'] = MagicMock()
sys.modules['pyaudio'] = MagicMock()

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if 'voice_recognizer' in sys.modules:
    del sys.modules['voice_recognizer']

try:
    from voice_recognizer import VoiceRecognizer
except ImportError:
    pass

class TestVoiceOptimization(unittest.TestCase):
    @patch('voice_recognizer.VoiceRecognizer._calibrate_microphone')
    def test_microphone_context_optimization(self, mock_calibrate):
        recognizer = VoiceRecognizer(offline_mode=False)

        # Setup mock microphone as context manager
        mock_mic = MagicMock()
        mock_mic.__enter__.return_value = "source"
        recognizer.microphone = mock_mic

        call_count = [0]

        def mock_listen(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] <= 3:
                raise mock_sr.WaitTimeoutError("timeout")
            elif call_count[0] == 4:
                raise Exception("critical error")
            else:
                recognizer.is_listening = False
                return MagicMock()

        recognizer.recognizer.listen.side_effect = mock_listen

        # Disable sleep to make test fast
        with patch('time.sleep'):
            recognizer.is_listening = True
            recognizer._listen_loop()

        # Without optimization: __enter__ called 5 times
        # With optimization: __enter__ called 2 times (once initially, once after critical error)

        print(f"__enter__ called {mock_mic.__enter__.call_count} times")
        self.assertEqual(mock_mic.__enter__.call_count, 2, "Microphone context should remain open during timeouts")

if __name__ == '__main__':
    unittest.main()
