import sys
import unittest
from unittest.mock import MagicMock, patch
import os

# Mock modules before importing project code
mock_sr = MagicMock()
sys.modules["speech_recognition"] = mock_sr
mock_pyaudio = MagicMock()
sys.modules["pyaudio"] = mock_pyaudio
mock_vosk = MagicMock()
sys.modules["vosk"] = mock_vosk
mock_cv2 = MagicMock()
sys.modules["cv2"] = mock_cv2
mock_np = MagicMock()
sys.modules["numpy"] = mock_np
mock_pyautogui = MagicMock()
sys.modules["pyautogui"] = mock_pyautogui

# Mock Exception for WaitTimeoutError
mock_sr.WaitTimeoutError = type('WaitTimeoutError', (Exception,), {})

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from voice_recognizer import VoiceRecognizer

class TestVoiceOptimization(unittest.TestCase):
    def setUp(self):
        # Reset mocks
        mock_sr.reset_mock()

        # Setup Microphone mock
        self.mock_mic_instance = MagicMock()
        mock_sr.Microphone.return_value = self.mock_mic_instance
        self.mock_mic_instance.__enter__.return_value = "source_mock"
        self.mock_mic_instance.__exit__.return_value = None

        # Setup Recognizer mock
        self.mock_recognizer_instance = MagicMock()
        mock_sr.Recognizer.return_value = self.mock_recognizer_instance

    def test_microphone_opened_once_in_loop(self):
        # Patch calibrate to avoid extra calls during init
        with patch.object(VoiceRecognizer, '_calibrate_microphone'):
            vr = VoiceRecognizer()
            vr.is_listening = True

            # Setup side effect to stop listening after 3 calls
            # This simulates the loop running 3 times
            def listen_side_effect(*args, **kwargs):
                if self.mock_recognizer_instance.listen.call_count >= 3:
                    vr.is_listening = False
                return MagicMock() # Return dummy audio data

            self.mock_recognizer_instance.listen.side_effect = listen_side_effect

            # Mock internal recognition to avoid complex logic
            vr._recognize_speech = MagicMock(return_value="test")
            vr._map_command_to_action = MagicMock(return_value="action")

            # Run the loop (blocking call since we invoke _listen_loop directly)
            vr._listen_loop()

            # Verify listen was called 3 times
            self.assertEqual(self.mock_recognizer_instance.listen.call_count, 3)

            # Check how many times microphone context manager was entered
            enter_calls = self.mock_mic_instance.__enter__.call_count
            print(f"Microphone.__enter__ called {enter_calls} times")

            # For optimization, we want exactly 1 call.
            # Currently (before fix), this should be 3.
            self.assertEqual(enter_calls, 1, f"Microphone should be opened only once, but was opened {enter_calls} times")

if __name__ == '__main__':
    unittest.main()
