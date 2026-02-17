
import sys
import time
import pytest
from unittest.mock import MagicMock

# Define behavior for WaitTimeoutError
class WaitTimeoutError(Exception):
    pass

# Mock Microphone to track usage
class MockMicrophone:
    def __init__(self):
        self.enter_count = 0
        self.exit_count = 0

    def __enter__(self):
        self.enter_count += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit_count += 1

# Mock Recognizer
class MockRecognizer:
    def __init__(self):
        self.energy_threshold = 300
        self.dynamic_energy_threshold = True
        self.pause_threshold = 0.8
        self.call_count = 0

    def adjust_for_ambient_noise(self, source, duration=1):
        pass

    def listen(self, source, timeout=None, phrase_time_limit=None):
        self.call_count += 1
        # Simulate timeout for the first few calls
        if self.call_count <= 3:
            raise WaitTimeoutError("Timeout")
        # Then return something
        return MagicMock()

    def recognize_google(self, audio, language="en-US"):
        return "test command"

# Setup mocks
@pytest.fixture(autouse=True)
def mock_dependencies():
    # Mock dependencies if not present
    if "cv2" not in sys.modules:
        sys.modules["cv2"] = MagicMock()
    if "numpy" not in sys.modules:
        sys.modules["numpy"] = MagicMock()
    if "pyautogui" not in sys.modules:
        sys.modules["pyautogui"] = MagicMock()
    if "vosk" not in sys.modules:
        sys.modules["vosk"] = MagicMock()

    # Mock speech_recognition
    sr = MagicMock()
    sr.WaitTimeoutError = WaitTimeoutError
    sr.Recognizer = MockRecognizer
    sr.Microphone = MockMicrophone
    sys.modules["speech_recognition"] = sr

    yield

def test_microphone_stream_persistence():
    """
    Test that the microphone stream is not constantly reopened (enter/exit)
    during the listening loop when timeouts occur.
    """
    # Import inside test to ensure mocks are active
    # We might need to reload if it was already imported
    if "voice_recognizer" in sys.modules:
        del sys.modules["voice_recognizer"]

    from voice_recognizer import VoiceRecognizer

    # Initialize
    vr = VoiceRecognizer()

    # Replace the microphone instance with our tracked mock
    mock_mic = MockMicrophone()
    vr.microphone = mock_mic

    # Start listening
    vr.start_listening()

    # Let it run for a bit (enough for 3 timeouts + 1 success)
    start_time = time.time()

    # Wait until listen has been called at least 4 times
    # This proves the loop is running and encountering timeouts
    while vr.recognizer.call_count < 4:
        time.sleep(0.1)
        if time.time() - start_time > 2:
            break

    vr.stop_listening()

    print(f"Listen called: {vr.recognizer.call_count} times")
    print(f"Microphone __enter__ called: {mock_mic.enter_count} times")
    print(f"Microphone __exit__ called: {mock_mic.exit_count} times")

    # Assertions
    assert vr.recognizer.call_count >= 4, "Loop did not run enough times"
    assert mock_mic.enter_count == 1, "Microphone stream was opened multiple times"
    # Exit might be 1 (normal stop) or more if we had exceptions (but we expect 1 here)
    assert mock_mic.exit_count == 1, "Microphone stream was closed unexpectedly"
