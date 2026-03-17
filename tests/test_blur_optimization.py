import sys
import unittest
from unittest.mock import MagicMock, patch
import os

# Mock modules before import
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

# Configure flip to return input frame (identity)
mock_cv2.flip.side_effect = lambda src, flipCode, dst=None: dst if dst is not None else src

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gesture_detector import GestureDetector

class TestBlurOptimization(unittest.TestCase):
    def test_in_place_gaussian_blur(self):
        detector = GestureDetector(processing_scale=0.5)
        frame = MagicMock()
        frame.shape = (480, 640, 3) # Height, Width, Channels

        mock_cv2.cvtColor.return_value = MagicMock()
        mock_gray_small = MagicMock()
        mock_cv2.resize.return_value = mock_gray_small

        # Call detect_gesture
        detector.detect_gesture(frame, draw_landmarks=False)

        # Verify blur is called with dst=gray_small
        self.assertTrue(mock_cv2.GaussianBlur.called)
        kwargs = mock_cv2.GaussianBlur.call_args[1]
        self.assertIn('dst', kwargs, "cv2.GaussianBlur should be called with 'dst' parameter for in-place optimization")
        self.assertEqual(kwargs['dst'], mock_gray_small, "dst should be gray_small")

if __name__ == '__main__':
    unittest.main()
