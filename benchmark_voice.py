import time
import sys
import threading
from unittest.mock import MagicMock, patch

# Setup mocks FIRST
mock_sr = MagicMock()
sys.modules['speech_recognition'] = mock_sr

class MockMicrophone:
    enter_count = 0
    exit_count = 0

    def __enter__(self):
        MockMicrophone.enter_count += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        MockMicrophone.exit_count += 1
        return False

# Setup sr mock attributes
mock_sr.Recognizer = MagicMock
mock_sr.Microphone = MockMicrophone
WaitTimeoutError = type('WaitTimeoutError', (Exception,), {})
mock_sr.WaitTimeoutError = WaitTimeoutError

# Mock cv2 and numpy so voice_recognizer doesn't fail importing controller/config
sys.modules['cv2'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['pyaudio'] = MagicMock()

import voice_recognizer

from voice_recognizer import VoiceRecognizer

def benchmark():
    print("Benchmarking VoiceRecognizer._listen_loop...")
    # Mock calibrate to not count enters
    with patch.object(VoiceRecognizer, '_calibrate_microphone'):
        vr = VoiceRecognizer(offline_mode=False)

    # Simulate a stream of timeouts
    def mock_listen(*args, **kwargs):
        time.sleep(0.01) # Simulate some work
        raise WaitTimeoutError()

    vr.recognizer.listen.side_effect = mock_listen

    # Start loop in thread
    vr.is_listening = True
    thread = threading.Thread(target=vr._listen_loop)
    thread.daemon = True

    start_time = time.time()
    thread.start()

    # Let it run for 1 second
    time.sleep(1)

    vr.is_listening = False
    thread.join(timeout=1)

    duration = time.time() - start_time

    print(f"Microphone context __enter__ called: {MockMicrophone.enter_count} times")
    print(f"Microphone context __exit__ called: {MockMicrophone.exit_count} times")

    if MockMicrophone.enter_count > 1:
        print("POTENTIAL OPTIMIZATION: Microphone stream is re-initialized on every loop iteration.")

if __name__ == "__main__":
    benchmark()
