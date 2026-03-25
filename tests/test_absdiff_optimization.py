import sys
import unittest
from unittest.mock import MagicMock
import os

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

# Configure flip
def mock_flip(src, flipCode, dst=None):
    if dst is not None:
        dst.shape = src.shape
        return dst
    return src
mock_cv2.flip.side_effect = mock_flip

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gesture_detector import GestureDetector

class TestAbsdiffOptimization(unittest.TestCase):
    def test_in_place_absdiff(self):
        detector = GestureDetector(processing_scale=0.5)
        frame = MagicMock()
        frame.shape = (480, 640, 3)

        mock_resized_gray = MagicMock()
        mock_resized_gray.shape = (240, 320)
        mock_cv2.resize.return_value = mock_resized_gray
        mock_cv2.GaussianBlur.return_value = mock_resized_gray

        mock_cv2.threshold.return_value = (None, MagicMock())
        mock_cv2.findContours.return_value = ([], None)
        detector.detect_gesture(frame, draw_landmarks=False)

        mock_frame_delta = MagicMock()
        mock_cv2.absdiff.return_value = mock_frame_delta

        # We need self.prev_frame to be a valid object to check if it's passed as dst
        prev_frame_mock = detector.prev_frame

        detector.detect_gesture(frame, draw_landmarks=False)

        self.assertTrue(mock_cv2.absdiff.called)
        kwargs = mock_cv2.absdiff.call_args[1]
        self.assertIn('dst', kwargs, "cv2.absdiff should be called with 'dst' parameter for in-place optimization")
        self.assertIs(kwargs['dst'], prev_frame_mock, "dst should be self.prev_frame to reuse the old frame buffer")

if __name__ == '__main__':
    unittest.main()
