import sys
import unittest
from unittest.mock import MagicMock, patch
import os
import json

# Mock dependencies before import
mock_sr = MagicMock()
sys.modules['speech_recognition'] = mock_sr

mock_vosk = MagicMock()
mock_vosk_model = MagicMock()
mock_vosk_kaldi = MagicMock()

# Configure the KaldiRecognizer mock
class MockKaldiRecognizer:
    def __init__(self, model, rate):
        self.model = model
        self.rate = rate
        self.reset_called = False
        self.accept_waveform_result = True
        self.result_text = json.dumps({"text": "test command"})

    def Reset(self):
        self.reset_called = True

    def AcceptWaveform(self, data):
        return self.accept_waveform_result

    def Result(self):
        return self.result_text

    def PartialResult(self):
        return json.dumps({"partial": "test"})

mock_vosk.Model = MagicMock(return_value=mock_vosk_model)
mock_vosk.KaldiRecognizer = MagicMock(side_effect=lambda m, r: MockKaldiRecognizer(m, r))

sys.modules['vosk'] = mock_vosk

# Mock other dependencies
sys.modules['cv2'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['pyaudio'] = MagicMock()

# Make sure we clean up any pre-loaded voice_recognizer
if 'voice_recognizer' in sys.modules:
    del sys.modules['voice_recognizer']

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import voice_recognizer
    # Set HAS_VOSK to True manually for the test
    voice_recognizer.HAS_VOSK = True
    from voice_recognizer import VoiceRecognizer
except ImportError as e:
    print(f"Could not import VoiceRecognizer: {e}")
    sys.exit(1)


class TestVoskOptimization(unittest.TestCase):
    @patch('os.path.exists', return_value=True)
    def test_vosk_recognizer_cached_and_reset(self, mock_exists):
        # Create a VR instance in offline mode
        # This should trigger _load_vosk_model
        vr = VoiceRecognizer(offline_mode=True)

        # Verify Model and KaldiRecognizer were instantiated once during init
        mock_vosk.Model.assert_called_once()
        mock_vosk.KaldiRecognizer.assert_called_once()

        # Verify it was cached
        self.assertIsNotNone(vr.vosk_recognizer)
        self.assertIsInstance(vr.vosk_recognizer, MockKaldiRecognizer)

        # Reset the KaldiRecognizer mock to track calls during recognition
        cached_recognizer = vr.vosk_recognizer
        cached_recognizer.reset_called = False

        # Create a mock audio object
        mock_audio = MagicMock()
        mock_audio.get_raw_data.return_value = b"fake_audio_data"

        # Call _recognize_with_vosk
        result1 = vr._recognize_with_vosk(mock_audio)

        # Verify result
        self.assertEqual(result1, "test command")

        # Verify Reset was called
        self.assertTrue(cached_recognizer.reset_called, ".Reset() must be called on the cached recognizer")

        # Reset tracker and call again
        cached_recognizer.reset_called = False
        mock_vosk.KaldiRecognizer.reset_mock() # Reset the class instantiation mock

        result2 = vr._recognize_with_vosk(mock_audio)

        # Verify KaldiRecognizer was NOT instantiated again
        mock_vosk.KaldiRecognizer.assert_not_called()

        # Verify Reset was called again
        self.assertTrue(cached_recognizer.reset_called, ".Reset() must be called on subsequent recognitions")
        self.assertEqual(result2, "test command")

if __name__ == '__main__':
    unittest.main()
