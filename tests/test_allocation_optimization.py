import sys
import unittest
from unittest.mock import MagicMock
import os

# Mock dependencies to prevent import errors
mock_cv2 = MagicMock()
sys.modules['cv2'] = mock_cv2
mock_np = MagicMock()
sys.modules['numpy'] = mock_np
sys.modules['speech_recognition'] = MagicMock()
sys.modules['pyaudio'] = MagicMock()
sys.modules['pyautogui'] = MagicMock()
sys.modules['winsound'] = MagicMock()
sys.modules['win32gui'] = MagicMock()
sys.modules['win32process'] = MagicMock()
sys.modules['psutil'] = MagicMock()

# Setup constants
mock_cv2.COLOR_BGR2GRAY = 6
mock_cv2.THRESH_BINARY = 0
mock_cv2.RETR_EXTERNAL = 0
mock_cv2.CHAIN_APPROX_SIMPLE = 2

# Configure mocks to return input or fake result
mock_cv2.flip.side_effect = lambda src, flipCode, dst=None: dst if dst is not None else src
mock_cv2.cvtColor.side_effect = lambda src, code, dst=None: dst if dst is not None else MagicMock()
mock_cv2.resize.side_effect = lambda src, dsize, dst=None: dst if dst is not None else MagicMock()
mock_cv2.GaussianBlur.side_effect = lambda src, ksize, sigmaX, dst=None: dst if dst is not None else src
mock_cv2.absdiff.side_effect = lambda src1, src2, dst=None: dst if dst is not None else MagicMock()
mock_cv2.threshold.return_value = (0, MagicMock())
mock_cv2.dilate.side_effect = lambda src, kernel, iterations=1, dst=None: dst if dst is not None else src
mock_cv2.findContours.return_value = ([], None)

def _mock_np_empty(shape, dtype=None):
    """Return a MagicMock that mimics a NumPy array with the requested shape.

    This allows GestureDetector.detect_gesture() to inspect buffer.shape
    and decide whether to reuse or reallocate buffers during tests.
    """
    arr = MagicMock()
    arr.shape = shape
    return arr

mock_np.empty.side_effect = _mock_np_empty
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    if 'gesture_detector' in sys.modules:
        del sys.modules['gesture_detector']
    from gesture_detector import GestureDetector
except ImportError as e:
    print(f"Could not import GestureDetector: {e}")
    sys.exit(1)


class TestAllocationOptimization(unittest.TestCase):
    def setUp(self):
        # Reset mocks
        mock_cv2.reset_mock()
        mock_np.reset_mock()

    def test_cvtColor_and_resize_use_dst(self):
        detector = GestureDetector(processing_scale=0.5)

        # Create a mock frame
        frame = MagicMock()
        frame.shape = (480, 640, 3)

        # Call detect_gesture
        detector.detect_gesture(frame, draw_landmarks=False)

        # Verify cvtColor was called with dst
        self.assertTrue(mock_cv2.cvtColor.called, "cv2.cvtColor was not called")
        cvtColor_kwargs = mock_cv2.cvtColor.call_args[1]
        self.assertIn('dst', cvtColor_kwargs, "cv2.cvtColor should use 'dst' parameter to avoid memory allocation")

        # Verify resize was called with dst
        self.assertTrue(mock_cv2.resize.called, "cv2.resize was not called")
        resize_kwargs = mock_cv2.resize.call_args[1]
        self.assertIn('dst', resize_kwargs, "cv2.resize should use 'dst' parameter to avoid memory allocation")

    def test_double_buffering_preserves_motion_detection(self):
        detector = GestureDetector(processing_scale=0.5)

        frame1 = MagicMock()
        frame1.shape = (480, 640, 3)

        frame2 = MagicMock()
        frame2.shape = (480, 640, 3)

        # First frame initializes the buffer
        detector.detect_gesture(frame1, draw_landmarks=False)

        # Second frame uses the other buffer and performs absdiff
        detector.detect_gesture(frame2, draw_landmarks=False)

        # Check that absdiff was called correctly
        self.assertTrue(mock_cv2.absdiff.called, "cv2.absdiff was not called on the second frame")

        # Verify double buffering ensures prev_frame is not pointing to the same array as current frame_small
        prev_frame_ref = mock_cv2.absdiff.call_args[0][0]
        curr_frame_ref = mock_cv2.absdiff.call_args[0][1]
        self.assertIsNot(prev_frame_ref, curr_frame_ref, "Double buffering failed: prev_frame and curr_frame point to the same array!")


if __name__ == '__main__':
    unittest.main()
