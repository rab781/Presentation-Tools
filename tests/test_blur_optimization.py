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
mock_np.empty_like.side_effect = lambda x: type('MockArray', (), {'shape': x.shape})()

# Setup mock constants
mock_cv2.COLOR_BGR2GRAY = 6
mock_cv2.THRESH_BINARY = 0
mock_cv2.RETR_EXTERNAL = 0
mock_cv2.CHAIN_APPROX_SIMPLE = 2

# Configure flip to return input frame (identity)
def mock_flip(src, flipCode, dst=None):
    if dst is not None:
        dst.shape = src.shape
        return dst
    return src
mock_cv2.flip.side_effect = mock_flip

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gesture_detector import GestureDetector

class TestBlurOptimization(unittest.TestCase):
    def test_in_place_gaussian_blur(self):
        detector = GestureDetector(processing_scale=0.5)
        frame = MagicMock()
        frame.shape = (480, 640, 3)

        # Call detect_gesture
        detector.detect_gesture(frame, draw_landmarks=False)

        # Verify GaussianBlur was called with dst
        self.assertTrue(mock_cv2.GaussianBlur.called, "cv2.GaussianBlur was not called")

        args = mock_cv2.GaussianBlur.call_args[0]
        kwargs = mock_cv2.GaussianBlur.call_args[1]

        self.assertIn('dst', kwargs, "cv2.GaussianBlur should use 'dst' parameter to avoid memory allocation")
        self.assertEqual(kwargs['dst'], args[0], "dst should be the same as the input array")

if __name__ == '__main__':
    unittest.main()
