import unittest
from unittest.mock import MagicMock, patch
import sys
import threading
import time

# Mock speech_recognition before importing voice_recognizer
mock_sr = MagicMock()
sys.modules["speech_recognition"] = mock_sr

# Define WaitTimeoutError on the mock so it can be caught
class WaitTimeoutError(Exception):
    pass
mock_sr.WaitTimeoutError = WaitTimeoutError

# Also mock pyaudio and vosk as they might be imported
sys.modules["pyaudio"] = MagicMock()
sys.modules["vosk"] = MagicMock()

# Now import the class under test
# We need to ensure we import it after mocking
if "voice_recognizer" in sys.modules:
    del sys.modules["voice_recognizer"]
from voice_recognizer import VoiceRecognizer

class TestVoiceOptimization(unittest.TestCase):
    def setUp(self):
        self.recognizer_mock = MagicMock()
        mock_sr.Recognizer.return_value = self.recognizer_mock

        self.microphone_mock = MagicMock()
        self.microphone_mock.__enter__ = MagicMock(return_value=MagicMock())
        self.microphone_mock.__exit__ = MagicMock(return_value=None)
        mock_sr.Microphone.return_value = self.microphone_mock

    def test_microphone_enter_count(self):
        """
        Verify that Microphone context is entered only once during listening loop,
        even if timeouts occur.
        """
        # Setup the mock to simulate timeouts then a stop
        # First call is calibration (in __init__) -> success
        # Next calls are in _listen_loop

        # We want to simulate the loop running for a few iterations
        # The loop condition is `self.is_listening`
        # We can simulate the loop by having `recognizer.listen` side effects

        # Scenario:
        # 1. calibrate (success)
        # 2. listen -> WaitTimeoutError
        # 3. listen -> WaitTimeoutError
        # 4. listen -> Stop (we'll set is_listening=False via side effect or thread)

        # To avoid infinite loop if code is buggy, we'll use a side effect that eventually stops

        vr = VoiceRecognizer(offline_mode=False)

        # Mock _calibrate_microphone to avoid the first __enter__ call counting towards our loop test?
        # Actually, let's just count total calls.
        # __init__ calls _calibrate_microphone -> 1 enter

        # Reset mock counts after init to focus on _listen_loop
        self.microphone_mock.__enter__.reset_mock()

        # Setup listen to raise timeout twice, then return audio
        # Then we stop the loop

        def listen_side_effect(*args, **kwargs):
            # Check how many times we've been called
            count = self.recognizer_mock.listen.call_count
            if count <= 2:
                raise mock_sr.WaitTimeoutError()
            else:
                vr.is_listening = False # Stop the loop
                return MagicMock() # Return dummy audio

        self.recognizer_mock.listen.side_effect = listen_side_effect

        # Start listening (this starts a thread)
        # We want to run `_listen_loop` synchronously for testing to be deterministic
        vr.is_listening = True
        vr._listen_loop()

        # Assertions
        # In the unoptimized code:
        # Loop 1 (timeout): enters context, listens, exits context
        # Loop 2 (timeout): enters context, listens, exits context
        # Loop 3 (success): enters context, listens, exits context
        # Total expected enters: 3

        # In the optimized code:
        # Enters context
        # Loop 1 (timeout): catch, continue (stay in context)
        # Loop 2 (timeout): catch, continue (stay in context)
        # Loop 3 (success): process, loop condition becomes false
        # Exits context
        # Total expected enters: 1

        count = self.microphone_mock.__enter__.call_count
        print(f"Microphone.__enter__ called {count} times")

        # Assert optimization works
        self.assertEqual(count, 1, "Microphone context should be entered only once during the loop")

if __name__ == '__main__':
    unittest.main()
