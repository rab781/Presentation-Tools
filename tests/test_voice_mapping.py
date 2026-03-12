import sys
import unittest
from unittest.mock import MagicMock
import os

# Mock dependencies before import
mock_sr = MagicMock()
sys.modules['speech_recognition'] = mock_sr

# Mock cv2 and numpy to prevent controller import errors
sys.modules['cv2'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['pyaudio'] = MagicMock()

class MockWaitTimeoutError(Exception):
    pass
mock_sr.WaitTimeoutError = MockWaitTimeoutError

# Make sure we clean up any pre-loaded voice_recognizer from sys.modules
if 'voice_recognizer' in sys.modules:
    del sys.modules['voice_recognizer']

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from voice_recognizer import VoiceRecognizer
from config import VOICE_COMMANDS


class TestVoiceMapping(unittest.TestCase):
    def setUp(self):
        # Prevent initialization of microphone stream
        self.mock_microphone = MagicMock()
        mock_sr.Microphone = MagicMock(return_value=self.mock_microphone)

        # Override _calibrate_microphone to do nothing
        self.original_calibrate = VoiceRecognizer._calibrate_microphone
        VoiceRecognizer._calibrate_microphone = MagicMock()

        self.vr = VoiceRecognizer(offline_mode=False)

    def tearDown(self):
        VoiceRecognizer._calibrate_microphone = self.original_calibrate

    def test_exact_match(self):
        # Exact keyword matches should resolve in O(1)
        self.assertEqual(self.vr._map_command_to_action("lanjut"), "next")
        self.assertEqual(self.vr._map_command_to_action("lanjutkan"), "play")
        self.assertEqual(self.vr._map_command_to_action("berhenti"), "pause")

    def test_overlapping_keywords(self):
        # Test that longer keywords take precedence over shorter ones
        # "lanjut" is mapped to "next", but "lanjutkan" is mapped to "play"
        # The substring "lanjut" is in "lanjutkan", so if sorted by length descending,
        # "lanjutkan" should match first.
        self.assertEqual(self.vr._map_command_to_action("tolong lanjutkan presentasi"), "play")

        # Test basic substring matches
        self.assertEqual(self.vr._map_command_to_action("tolong lanjut ke slide"), "next")

        # Test with case and whitespace
        self.assertEqual(self.vr._map_command_to_action(" LanjutKan   "), "play")

    def test_multi_word_commands(self):
        self.assertEqual(self.vr._map_command_to_action("bisa kembali ke awal"), "previous")
        self.assertEqual(self.vr._map_command_to_action("mari kita mulai saja"), "first")

    def test_no_match(self):
        self.assertIsNone(self.vr._map_command_to_action(""))
        self.assertIsNone(self.vr._map_command_to_action("kata tidak dikenal"))


if __name__ == '__main__':
    unittest.main()
