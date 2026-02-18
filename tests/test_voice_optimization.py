import sys
import unittest
from unittest.mock import MagicMock
import time
import threading
import os

# Mock modules before import
mock_sr = MagicMock()
sys.modules["speech_recognition"] = mock_sr
mock_vosk = MagicMock()
sys.modules["vosk"] = mock_vosk

# Define WaitTimeoutError for mock
class WaitTimeoutError(Exception):
    pass
mock_sr.WaitTimeoutError = WaitTimeoutError

# Mock Microphone
class MockMicrophone:
    def __init__(self):
        self.enter_count = 0
        self.exit_count = 0

    def __enter__(self):
        self.enter_count += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit_count += 1

# Setup imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from voice_recognizer import VoiceRecognizer
except ImportError:
    print("Failed to import VoiceRecognizer")
    sys.exit(1)

class TestVoiceOptimization(unittest.TestCase):
    def setUp(self):
        # Create a fresh mock microphone for each test
        self.mock_mic = MockMicrophone()
        # Ensure sr.Microphone() returns this instance
        mock_sr.Microphone.return_value = self.mock_mic

        # Reset Recognizer
        self.mock_recognizer = MagicMock()
        mock_sr.Recognizer.return_value = self.mock_recognizer
        self.mock_recognizer.recognize_google.return_value = "test"

        # Setup listen mock to timeout first, then succeed
        self.call_count = 0
        def mock_listen(source, timeout=None, phrase_time_limit=None):
            self.call_count += 1
            # First 2 calls timeout, subsequent calls return a mock audio
            if self.call_count <= 2:
                raise WaitTimeoutError("Timeout")
            return MagicMock()

        self.mock_recognizer.listen.side_effect = mock_listen

    def test_single_stream_initialization(self):
        """Test that microphone stream is initialized only once during listening loop"""
        # Initialize VoiceRecognizer (this will trigger calibration and one enter/exit)
        vr = VoiceRecognizer(offline_mode=False)

        # Reset counters to ignore initialization calls
        self.mock_mic.enter_count = 0
        self.mock_mic.exit_count = 0
        self.call_count = 0

        # Start listening in a thread
        vr.is_listening = True
        thread = threading.Thread(target=vr._listen_loop)
        thread.start()

        # Wait for loop to cycle a few times
        # We want to ensure at least 3 listen calls (2 timeouts + 1 success)
        start_time = time.time()
        while self.call_count < 3 and (time.time() - start_time) < 2:
            time.sleep(0.05)

        # Stop listening
        vr.is_listening = False
        thread.join(timeout=1)

        # Verify call counts
        # We expect at least 3 listen calls
        self.assertGreaterEqual(self.call_count, 3, "Should have called listen multiple times")

        # We expect exactly 1 enter call (stream opened once)
        self.assertEqual(self.mock_mic.enter_count, 1,
                        f"Microphone stream re-opened {self.mock_mic.enter_count} times! Should be 1.")

        # We expect 1 exit call (stream closed once at end)
        self.assertEqual(self.mock_mic.exit_count, 1,
                        "Microphone stream should be closed exactly once.")

if __name__ == '__main__':
    unittest.main()
