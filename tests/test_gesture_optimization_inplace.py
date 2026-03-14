import sys
import unittest
from unittest.mock import MagicMock, patch
import os

# Mock modules before import
# To ensure test isolation, we remove modules from sys.modules
for mod in ["cv2", "numpy", "gesture_detector", "config", "controller"]:
    if mod in sys.modules:
        del sys.modules[mod]

mock_cv2 = MagicMock()
sys.modules["cv2"] = mock_cv2
mock_np = MagicMock()
sys.modules["numpy"] = mock_np

# Setup mock constants
mock_cv2.COLOR_BGR2GRAY = 6
mock_cv2.THRESH_BINARY = 0
mock_cv2.RETR_EXTERNAL = 0
mock_cv2.CHAIN_APPROX_SIMPLE = 2

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from gesture_detector import GestureDetector
except ImportError:
    # If import fails (e.g. because of other dependencies), we can't run tests
    print("Could not import gesture_detector. Dependencies might be missing even with mocks.")
    sys.exit(1)

class TestGestureOptimizationInplace(unittest.TestCase):
    def setUp(self):
        # Reset mocks
        mock_cv2.reset_mock()
        mock_np.reset_mock()
        # Configure flip to return input frame (identity)
        mock_cv2.flip.side_effect = lambda src, flipCode, dst=None: dst if dst is not None else src

    def test_in_place_threshold_dilate(self):
        detector = GestureDetector(processing_scale=0.5)
        frame = MagicMock()
        frame.shape = (480, 640, 3) # Height, Width, Channels

        # Call 1: Set prev_frame
        detector.detect_gesture(frame, draw_landmarks=False)

        # Call 2: Trigger logic
        mock_frame_delta = MagicMock()
        mock_thresh_res = MagicMock()
        mock_cv2.absdiff.return_value = mock_frame_delta
        mock_cv2.threshold.return_value = (None, mock_thresh_res)
        mock_cv2.findContours.return_value = ([], None)

        detector.detect_gesture(frame, draw_landmarks=False)

        # Verify threshold is called with dst=frame_delta
        self.assertTrue(mock_cv2.threshold.called)
        kwargs = mock_cv2.threshold.call_args[1]
        self.assertIn('dst', kwargs, "cv2.threshold should be called with 'dst' parameter for in-place optimization")
        self.assertEqual(kwargs['dst'], mock_frame_delta, "dst should be frame_delta")

        # Verify dilate is called with dst=thresh
        self.assertTrue(mock_cv2.dilate.called)
        kwargs = mock_cv2.dilate.call_args[1]
        self.assertIn('dst', kwargs, "cv2.dilate should be called with 'dst' parameter for in-place optimization")
        self.assertEqual(kwargs['dst'], mock_thresh_res, "dst should be thresh")

if __name__ == '__main__':
    unittest.main()
