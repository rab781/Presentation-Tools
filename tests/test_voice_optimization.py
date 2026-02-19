import sys
import unittest
from unittest.mock import MagicMock, patch, ANY
import os

# Mock modules before import
mock_sr = MagicMock()
sys.modules["speech_recognition"] = mock_sr
mock_pyaudio = MagicMock()
sys.modules["pyaudio"] = mock_pyaudio
mock_vosk = MagicMock()
sys.modules["vosk"] = mock_vosk

# Define WaitTimeoutError on the mock so it can be caught
class MockWaitTimeoutError(Exception):
    pass
mock_sr.WaitTimeoutError = MockWaitTimeoutError
mock_sr.UnknownValueError = Exception
mock_sr.RequestError = Exception

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module under test
# We need to ensure config is imported correctly or mocked if needed
# config.py seems to not have side effects that block execution, so we let it import.
try:
    from voice_recognizer import VoiceRecognizer
except ImportError:
    print("Could not import voice_recognizer. Dependencies might be missing even with mocks.")
    sys.exit(1)

class TestVoiceOptimization(unittest.TestCase):
    def setUp(self):
        # Reset mocks
        mock_sr.reset_mock()

        # Setup Microphone mock
        self.mock_microphone_instance = MagicMock()
        mock_sr.Microphone.return_value = self.mock_microphone_instance

        # Setup Recognizer mock
        self.mock_recognizer_instance = MagicMock()
        mock_sr.Recognizer.return_value = self.mock_recognizer_instance

        # Initial config for recognizer attributes
        self.mock_recognizer_instance.energy_threshold = 4000
        self.mock_recognizer_instance.dynamic_energy_threshold = True
        self.mock_recognizer_instance.pause_threshold = 0.8

    def test_listen_loop_microphone_enter_count(self):
        """
        Test that Microphone.__enter__ is called only once during the listen loop,
        even if multiple listen attempts occur.
        """
        recognizer = VoiceRecognizer(offline_mode=False)

        # Reset mock calls from __init__ (calibration calls __enter__)
        self.mock_microphone_instance.__enter__.reset_mock()

        # Configure the listen loop behavior
        # We want to simulate the loop running for a few iterations
        # The loop condition is `while self.is_listening:`
        # We can simulate this by side_effect on `recognizer.listen`

        # Side effect function to control loop
        iteration_count = 0
        def listen_side_effect(source, timeout=None, phrase_time_limit=None):
            nonlocal iteration_count
            iteration_count += 1
            if iteration_count >= 3:
                # Stop listening after 3 iterations
                recognizer.is_listening = False

            # Simulate timeout (common case)
            raise mock_sr.WaitTimeoutError("Timeout")

        self.mock_recognizer_instance.listen.side_effect = listen_side_effect

        # Start listening (manually call _listen_loop to avoid threading complexity in test)
        recognizer.is_listening = True
        recognizer._listen_loop()

        # Verification
        # In optimized code, __enter__ should be called exactly ONCE.
        # In unoptimized code, it is called once per iteration (3 times).

        enter_call_count = self.mock_microphone_instance.__enter__.call_count
        print(f"Microphone.__enter__ called {enter_call_count} times")

        # Assert that it is called exactly once (Goal state)
        # This assertion will fail initially, confirming the opportunity for optimization.
        self.assertEqual(enter_call_count, 1,
                         f"Microphone should be opened only once, but was opened {enter_call_count} times")

if __name__ == '__main__':
    unittest.main()
