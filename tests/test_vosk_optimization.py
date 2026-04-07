import sys
import unittest
from unittest.mock import MagicMock, patch
import os
import json

# Mock dependencies before import
mock_sr = MagicMock()
sys.modules['speech_recognition'] = mock_sr

# Mock cv2 and numpy to prevent controller import errors
sys.modules['cv2'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['pyaudio'] = MagicMock()

# Setup vosk mock
mock_vosk = MagicMock()
mock_vosk.Model = MagicMock()
mock_vosk.KaldiRecognizer = MagicMock()
sys.modules['vosk'] = mock_vosk

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

class TestVoskOptimization(unittest.TestCase):
    @patch('voice_recognizer.VoiceRecognizer._calibrate_microphone')
    @patch('os.path.exists', return_value=True)
    def test_kaldi_recognizer_caching(self, mock_exists, mock_calibrate):
        vr = VoiceRecognizer(offline_mode=True)
        vr.vosk_model = MagicMock() # Ensure model is present

        mock_audio = MagicMock()
        mock_audio.get_raw_data.return_value = b'raw_data'

        # Reset mock call count
        mock_vosk.KaldiRecognizer.reset_mock()

        # Mock the recognizer instance behavior
        mock_rec_instance = MagicMock()
        mock_rec_instance.AcceptWaveform.return_value = True
        mock_rec_instance.Result.return_value = json.dumps({"text": "test command"})
        mock_vosk.KaldiRecognizer.return_value = mock_rec_instance

        # Call first time
        result1 = vr._recognize_with_vosk(mock_audio)
        self.assertEqual(result1, "test command")
        self.assertEqual(mock_vosk.KaldiRecognizer.call_count, 1, "KaldiRecognizer should be instantiated the first time")

        # Call second time
        result2 = vr._recognize_with_vosk(mock_audio)
        self.assertEqual(result2, "test command")
        self.assertEqual(mock_vosk.KaldiRecognizer.call_count, 1, "KaldiRecognizer should NOT be instantiated again")

        # Verify Reset was called
        self.assertTrue(mock_rec_instance.Reset.called, "Reset() should be called on the cached recognizer to prevent cross-utterance bleeding")

if __name__ == '__main__':
    unittest.main()
