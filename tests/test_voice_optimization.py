import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock modules
mock_sr = MagicMock()
sys.modules["speech_recognition"] = mock_sr
sys.modules["pyaudio"] = MagicMock()
sys.modules["vosk"] = MagicMock()

# Setup exceptions
class WaitTimeoutError(Exception):
    pass
mock_sr.WaitTimeoutError = WaitTimeoutError

# Import target module
try:
    from voice_recognizer import VoiceRecognizer
except ImportError:
    print("Could not import voice_recognizer")
    sys.exit(1)

class TestVoiceOptimization(unittest.TestCase):
    def setUp(self):
        # Reset mocks
        mock_sr.reset_mock()
        self.recognizer = VoiceRecognizer()

        # Reset again for clean state after init (which calls calibration)
        self.recognizer.recognizer = MagicMock()
        self.recognizer.microphone = MagicMock()
        self.recognizer.microphone.__enter__.return_value = "source"
        self.recognizer.microphone.__exit__.return_value = None

        # Mock other methods to avoid side effects
        self.recognizer._recognize_speech = MagicMock(return_value="test")
        self.recognizer._map_command_to_action = MagicMock(return_value="action")
        self.recognizer.command_queue = MagicMock()

    def test_microphone_enter_count(self):
        """Test that microphone context is entered multiple times (unoptimized)"""

        # We simulate 3 listen calls
        # 1. Success
        # 2. Timeout
        # 3. Success -> then stop

        iteration_count = 0

        def listen_side_effect(source, timeout=1, phrase_time_limit=3):
            nonlocal iteration_count
            iteration_count += 1

            if iteration_count == 1:
                return "audio1"
            elif iteration_count == 2:
                raise WaitTimeoutError()
            elif iteration_count == 3:
                self.recognizer.is_listening = False # Stop loop after this
                return "audio2"
            else:
                self.recognizer.is_listening = False
                return None

        self.recognizer.recognizer.listen.side_effect = listen_side_effect
        self.recognizer.is_listening = True

        # Run _listen_loop directly
        self.recognizer._listen_loop()

        # Verify loop ran 3 times
        self.assertEqual(self.recognizer.recognizer.listen.call_count, 3)

        # Verify microphone context was entered
        # In current unoptimized code: entered once per iteration = 3 times
        # In optimized code: entered once total = 1 time
        enter_count = self.recognizer.microphone.__enter__.call_count
        print(f"Microphone entered {enter_count} times during loop")

        # For optimized behavior, we expect it to be entered ONCE for the whole loop
        self.assertEqual(enter_count, 1, "Microphone context should be entered only once")

if __name__ == '__main__':
    unittest.main()
