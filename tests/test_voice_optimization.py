import sys
import unittest
from unittest.mock import MagicMock, patch
import threading
import time

# Mock modules before import
mock_sr = MagicMock()
sys.modules["speech_recognition"] = mock_sr
mock_vosk = MagicMock()
sys.modules["vosk"] = mock_vosk

# Configure WaitTimeoutError as an actual exception so we can catch it
class MockWaitTimeoutError(Exception):
    pass
mock_sr.WaitTimeoutError = MockWaitTimeoutError

import voice_recognizer
from voice_recognizer import VoiceRecognizer

class TestVoiceOptimization(unittest.TestCase):
    def setUp(self):
        # Reset mocks
        mock_sr.reset_mock()

        # Setup Microphone mock
        self.mock_microphone = MagicMock()
        self.mock_microphone.__enter__ = MagicMock(return_value=self.mock_microphone)
        self.mock_microphone.__exit__ = MagicMock(return_value=None)
        mock_sr.Microphone.return_value = self.mock_microphone

        # Setup Recognizer mock
        self.mock_recognizer = MagicMock()
        mock_sr.Recognizer.return_value = self.mock_recognizer

        # Prevent actual thread starting
        self.original_thread = threading.Thread
        threading.Thread = MagicMock()

    def tearDown(self):
        threading.Thread = self.original_thread

    def test_listen_loop_reopens_stream_continuously(self):
        """
        Verify that the current implementation re-opens the microphone stream
        on every iteration of the listening loop.
        """
        # Initialize recognizer
        # Mock _calibrate_microphone to avoid extra calls to __enter__
        with patch.object(VoiceRecognizer, '_calibrate_microphone'):
            vr = VoiceRecognizer(offline_mode=False)

        # Setup the loop to run 3 times
        # We use a side effect on listen() to control the loop
        # It raises WaitTimeoutError twice, then stops the loop

        iteration_count = 0
        def listen_side_effect(*args, **kwargs):
            nonlocal iteration_count
            iteration_count += 1
            if iteration_count < 3:
                raise mock_sr.WaitTimeoutError()
            else:
                vr.is_listening = False # Stop the loop
                raise mock_sr.WaitTimeoutError() # Raise one last time to hit continue/break

        self.mock_recognizer.listen.side_effect = listen_side_effect

        # Start listening (simulate thread)
        vr.is_listening = True
        vr._listen_loop()

        # Verification
        # In unoptimized code:
        # Loop 1: enter -> listen (timeout) -> exit
        # Loop 2: enter -> listen (timeout) -> exit
        # Loop 3: enter -> listen (stops) -> exit
        # Total __enter__ calls should be 3

        # In optimized code:
        # Enter
        # Loop 1: listen (timeout)
        # Loop 2: listen (timeout)
        # Loop 3: listen (stops)
        # Exit
        # Total __enter__ calls should be 1

        print(f"Microphone.__enter__ call count: {self.mock_microphone.__enter__.call_count}")

        # This assertion expects the *Optimized* behavior (1 call).
        # Since we haven't optimized it yet, this test should FAIL.
        self.assertEqual(self.mock_microphone.__enter__.call_count, 1,
                         "Microphone stream should be opened only once during the loop")

if __name__ == '__main__':
    unittest.main()
