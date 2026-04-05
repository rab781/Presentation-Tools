import sys
import unittest
from unittest.mock import MagicMock, patch
import os
import json

# Mock dependencies before import
mock_sr = MagicMock()
sys.modules['speech_recognition'] = mock_sr

sys.modules['cv2'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['pyaudio'] = MagicMock()

# Mock Vosk
mock_vosk = MagicMock()
mock_model = MagicMock()
mock_kaldi = MagicMock()

mock_vosk.Model = MagicMock(return_value=mock_model)
mock_vosk.KaldiRecognizer = MagicMock(return_value=mock_kaldi)
sys.modules['vosk'] = mock_vosk

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from voice_recognizer import VoiceRecognizer, HAS_VOSK

class TestVoskOptimization(unittest.TestCase):
    def setUp(self):
        mock_vosk.KaldiRecognizer.reset_mock()
        mock_kaldi.reset_mock()
        mock_vosk.Model.reset_mock()

    @unittest.skipIf(not HAS_VOSK, "Vosk not installed")
    @patch('os.path.exists', return_value=True)
    def test_kaldi_recognizer_caching_and_reset(self, mock_exists):
        # Create recognizer with offline mode to trigger _load_vosk_model
        vr = VoiceRecognizer(offline_mode=True)

        # Verify Model and KaldiRecognizer were instantiated once during setup
        mock_vosk.Model.assert_called_once()
        mock_vosk.KaldiRecognizer.assert_called_once()
        self.assertTrue(hasattr(vr, 'vosk_recognizer'))

        # Setup mock audio data and KaldiRecognizer behavior
        mock_audio = MagicMock()
        mock_audio.get_raw_data.return_value = b"mock_data"

        # First utterance
        mock_kaldi.AcceptWaveform.return_value = True
        mock_kaldi.Result.return_value = json.dumps({"text": "test one"})
        res1 = vr._recognize_with_vosk(mock_audio)
        self.assertEqual(res1, "test one")

        # Verify Reset was called
        self.assertEqual(mock_kaldi.Reset.call_count, 1)

        # Second utterance
        mock_kaldi.AcceptWaveform.return_value = True
        mock_kaldi.Result.return_value = json.dumps({"text": "test two"})
        res2 = vr._recognize_with_vosk(mock_audio)
        self.assertEqual(res2, "test two")

        # Verify Reset was called again
        self.assertEqual(mock_kaldi.Reset.call_count, 2)

        # Verify KaldiRecognizer was NOT instantiated again during recognition
        mock_vosk.KaldiRecognizer.assert_called_once()

if __name__ == '__main__':
    unittest.main()
