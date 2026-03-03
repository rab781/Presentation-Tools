import sys
import unittest
from unittest.mock import MagicMock, patch
import os
import time

# Mock dependencies before import
mock_sr = MagicMock()
sys.modules['speech_recognition'] = mock_sr

# Mock cv2 and numpy to prevent controller import errors
sys.modules['cv2'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['pyaudio'] = MagicMock()

# Setup sr mock attributes
mock_sr.Recognizer = MagicMock
# Create an exception class for WaitTimeoutError so it behaves like one
class MockWaitTimeoutError(Exception):
    pass
mock_sr.WaitTimeoutError = MockWaitTimeoutError

class MockMicrophoneContextManager:
    def __init__(self):
        self.enter_count = 0
        self.exit_count = 0

    def __enter__(self):
        self.enter_count += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit_count += 1
        return False # Don't suppress exceptions

mock_sr.Microphone = MockMicrophoneContextManager

# Make sure we clean up any pre-loaded voice_recognizer from sys.modules
if 'voice_recognizer' in sys.modules:
    del sys.modules['voice_recognizer']

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from voice_recognizer import VoiceRecognizer
except ImportError as e:
    print(f"Could not import VoiceRecognizer: {e}")
    sys.exit(1)


class TestVoiceOptimization(unittest.TestCase):
    def setUp(self):
        # Reset enter/exit counts
        pass

    @patch('voice_recognizer.VoiceRecognizer._calibrate_microphone')
    def test_microphone_context_optimization(self, mock_calibrate):
        # Test that the microphone stream stays open during timeouts
        # Instantiate recognizer
        vr = VoiceRecognizer(offline_mode=False)

        # Reset counts for the specific instance created
        vr.microphone.enter_count = 0
        vr.microphone.exit_count = 0

        # Create a mock listen function that raises WaitTimeoutError multiple times, then stops the loop
        call_count = [0]
        def mock_listen(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] >= 5:
                vr.is_listening = False
            raise mock_sr.WaitTimeoutError()

        vr.recognizer.listen.side_effect = mock_listen

        # Run the loop directly (not in a thread for testing predictability)
        vr.is_listening = True
        vr._listen_loop()

        # Verification:
        # listen() was called 5 times
        self.assertEqual(call_count[0], 5, "listen should have been called 5 times")

        # The context manager should have been entered EXACTLY ONCE
        # instead of 5 times
        self.assertEqual(vr.microphone.enter_count, 1,
                         "Microphone should only be initialized once during continuous silence")

    @patch('voice_recognizer.VoiceRecognizer._calibrate_microphone')
    @patch('time.sleep', return_value=None) # Don't actually sleep during test
    def test_microphone_reinitialization_on_error(self, mock_sleep, mock_calibrate):
        # Test that a hard error breaks the inner loop and forces re-initialization
        vr = VoiceRecognizer(offline_mode=False)
        vr.microphone.enter_count = 0
        vr.microphone.exit_count = 0

        call_count = [0]
        def mock_listen_with_error(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                # First call: timeout (stays in loop)
                raise mock_sr.WaitTimeoutError()
            elif call_count[0] == 2:
                # Second call: Hard error (should break inner loop and re-enter)
                raise RuntimeError("Microphone disconnected")
            elif call_count[0] == 3:
                # Third call: stop listening
                vr.is_listening = False
                raise mock_sr.WaitTimeoutError()

        vr.recognizer.listen.side_effect = mock_listen_with_error

        vr.is_listening = True
        vr._listen_loop()

        # Because of the hard error on the second call, the inner loop should have broken,
        # the context exited, and the outer loop should have re-entered the context for call 3.
        self.assertEqual(vr.microphone.enter_count, 2,
                         "Microphone should be re-initialized after a hard error")

if __name__ == '__main__':
    unittest.main()
