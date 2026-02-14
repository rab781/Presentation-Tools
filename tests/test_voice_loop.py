import unittest
from unittest.mock import MagicMock, patch
import sys
import threading
import time

# Mock dependencies before importing project modules
sys.modules['speech_recognition'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['pyautogui'] = MagicMock()
sys.modules['vosk'] = MagicMock()

# Now import the module to test
# We need to mock config as well since VoiceRecognizer imports it
with patch.dict(sys.modules, {'config': MagicMock()}):
    from voice_recognizer import VoiceRecognizer

class TestVoiceLoop(unittest.TestCase):
    def setUp(self):
        # Setup mocks
        self.mock_sr = sys.modules['speech_recognition']
        self.mock_sr.Recognizer = MagicMock()
        self.mock_sr.Microphone = MagicMock()

        # Setup specific behavior for Microphone context manager
        self.mock_mic_instance = self.mock_sr.Microphone.return_value
        self.mock_mic_instance.__enter__.return_value = "mock_source"
        self.mock_mic_instance.__exit__.return_value = None

        # Setup Recognizer behavior
        self.mock_recognizer_instance = self.mock_sr.Recognizer.return_value
        self.mock_recognizer_instance.listen.return_value = "mock_audio"
        self.mock_recognizer_instance.recognize_google.return_value = "test command"

        # Create instance
        self.voice_recognizer = VoiceRecognizer(offline_mode=False)
        # Prevent actual thread start in tests usually, but here we want to test the loop logic
        # We will run the loop manually or in a controlled thread

    def test_listen_loop_optimization(self):
        """Verify that microphone stream is opened only once for multiple listen calls"""

        # We'll run the loop in a separate thread but control it
        self.voice_recognizer.is_listening = True

        # We need to stop the loop after a few iterations
        # We can do this by having side_effect on listen check a counter

        iteration_count = 0
        def listen_side_effect(*args, **kwargs):
            nonlocal iteration_count
            iteration_count += 1
            if iteration_count >= 3:
                self.voice_recognizer.is_listening = False
            return "mock_audio"

        self.mock_recognizer_instance.listen.side_effect = listen_side_effect

        # Reset mock counts before running loop to ignore _calibrate_microphone calls
        self.mock_mic_instance.__enter__.reset_mock()
        self.mock_mic_instance.__exit__.reset_mock()
        self.mock_recognizer_instance.listen.reset_mock()

        # Run the loop directly (blocking)
        self.voice_recognizer._listen_loop()

        # Verification
        # 1. Check that __enter__ was called EXACTLY ONCE
        self.mock_mic_instance.__enter__.assert_called_once()

        # 2. Check that listen was called 3 times
        self.assertEqual(self.mock_recognizer_instance.listen.call_count, 3)

        # 3. Check that __exit__ was called EXACTLY ONCE
        self.mock_mic_instance.__exit__.assert_called_once()

if __name__ == '__main__':
    unittest.main()
