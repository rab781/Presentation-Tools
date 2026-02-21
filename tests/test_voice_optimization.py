import unittest
from unittest.mock import MagicMock
import sys

# Mock speech_recognition before importing voice_recognizer
# Create a dummy module for speech_recognition
sr_mock = MagicMock()
sys.modules["speech_recognition"] = sr_mock

# Define exceptions
class WaitTimeoutError(Exception):
    pass
class UnknownValueError(Exception):
    pass
class RequestError(Exception):
    pass

sr_mock.WaitTimeoutError = WaitTimeoutError
sr_mock.UnknownValueError = UnknownValueError
sr_mock.RequestError = RequestError

# Also need to mock config
config_mock = MagicMock()
sys.modules["config"] = config_mock
config_mock.VOICE_COMMANDS = {}
config_mock.VOICE_CONFIG = {"energy_threshold": 4000}

# Now import the module under test
# We need to make sure we reload it if it was already imported, or just import it now.
if "voice_recognizer" in sys.modules:
    del sys.modules["voice_recognizer"]

from voice_recognizer import VoiceRecognizer

class TestVoiceOptimization(unittest.TestCase):
    def test_microphone_enter_called_once_optimized(self):
        """Test that Microphone.__enter__ is called exactly once with optimization"""
        # Setup
        recognizer = VoiceRecognizer(offline_mode=False)

        # Create a fresh mock for microphone instance
        mic_instance = MagicMock()
        recognizer.microphone = mic_instance

        # Setup context manager mock
        enter_mock = MagicMock()
        mic_instance.__enter__ = enter_mock
        mic_instance.__exit__ = MagicMock()

        # Setup listen to simulate behavior:
        # 1. Timeout
        # 2. Timeout
        # 3. Success (returns audio)
        # 4. Stop loop

        call_count_wrapper = {'count': 0}

        def listen_side_effect(*args, **kwargs):
            call_count_wrapper['count'] += 1
            if call_count_wrapper['count'] <= 2:
                raise sr_mock.WaitTimeoutError()
            elif call_count_wrapper['count'] == 3:
                return MagicMock() # Audio data
            else:
                recognizer.is_listening = False
                return MagicMock()

        recognizer.recognizer.listen.side_effect = listen_side_effect

        # Prevent actual recognition from doing anything
        recognizer._recognize_speech = MagicMock(return_value=None)

        recognizer.is_listening = True

        # Run the loop directly
        recognizer._listen_loop()

        print(f"Microphone.__enter__ call count: {enter_mock.call_count}")

        # In optimized code, expected call count is 1.
        self.assertEqual(enter_mock.call_count, 1, f"Microphone context should be entered exactly once, but was entered {enter_mock.call_count} times")

if __name__ == '__main__':
    unittest.main()
