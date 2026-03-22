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

        # Create multiple frames of the same size to exercise the buffering logic
        frame1 = MagicMock()
        frame1.shape = (480, 640, 3)

        frame2 = MagicMock()
        frame2.shape = (480, 640, 3)

        frame3 = MagicMock()
        frame3.shape = (480, 640, 3)

        frame4 = MagicMock()
        frame4.shape = (480, 640, 3)

        # Process several frames to allow the implementation to alternate buffers
        detector.detect_gesture(frame1, draw_landmarks=False)
        detector.detect_gesture(frame2, draw_landmarks=False)
        detector.detect_gesture(frame3, draw_landmarks=False)
        detector.detect_gesture(frame4, draw_landmarks=False)

        # Check that absdiff was called (motion comparison is performed)
        self.assertTrue(mock_cv2.absdiff.called, "cv2.absdiff was not called for motion detection")

        # Extract the dst buffers used for resize across all calls
        resize_calls = mock_cv2.resize.call_args_list
        self.assertGreaterEqual(len(resize_calls), 3, "Expected cv2.resize to be called at least 3 times for double buffering validation")

        dst_buffers = []
        for _, kwargs in resize_calls:
            self.assertIn("dst", kwargs, "cv2.resize should use 'dst' parameter to avoid memory allocation")
            dst_buffers.append(kwargs["dst"])

        # There should be exactly two buffers that are reused
        unique_buffers = set(dst_buffers)
        self.assertEqual(
            len(unique_buffers),
            2,
            f"Expected exactly 2 dst buffers for double buffering, got {len(unique_buffers)}",
        )

        # Verify that the buffers alternate: A, B, A, B, ...
        for i in range(2, len(dst_buffers)):
            self.assertIs(
                dst_buffers[i],
                dst_buffers[i - 2],
                "Double buffering failed: dst buffer at position {i} does not match buffer two steps earlier",
            )
            self.assertIsNot(
                dst_buffers[i],
                dst_buffers[i - 1],
                "Double buffering failed: consecutive dst buffers should be different",
            )
if __name__ == '__main__':
    unittest.main()
