import sys
import unittest
from unittest.mock import MagicMock, patch
import os

# Mock modules before import
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

class TestGestureOptimization(unittest.TestCase):
    def setUp(self):
        # Reset mocks
        mock_cv2.reset_mock()
        mock_np.reset_mock()
        # Configure flip to return input frame (identity)
        mock_cv2.flip.side_effect = lambda src, flipCode, dst=None: dst if dst is not None else src

    def test_initialization_defaults(self):
        detector = GestureDetector()
        self.assertEqual(detector.processing_scale, 0.5)

    def test_initialization_custom_scale(self):
        detector = GestureDetector(processing_scale=0.25)
        self.assertEqual(detector.processing_scale, 0.25)

    def test_resize_called_with_correct_dimensions(self):
        detector = GestureDetector(processing_scale=0.5)
        frame = MagicMock()
        frame.shape = (480, 640, 3) # Height, Width, Channels

        # Setup mock returns
        mock_cv2.cvtColor.return_value = MagicMock()
        mock_cv2.resize.return_value = MagicMock()

        # Call detect_gesture
        detector.detect_gesture(frame, draw_landmarks=False)

        # Verify resize call
        # Expected size: width=320 (640*0.5), height=240 (480*0.5)
        # Note: cv2.resize takes (width, height)
        mock_cv2.resize.assert_called_with(mock_cv2.cvtColor.return_value, (320, 240))

    def test_coordinate_scaling(self):
        detector = GestureDetector(processing_scale=0.5)
        frame = MagicMock()
        frame.shape = (480, 640, 3)

        # First call to initialize prev_frame
        mock_cv2.resize.return_value = MagicMock() # gray_small
        detector.detect_gesture(frame, draw_landmarks=False)

        # Second call to trigger logic
        # Mock finding contours
        contour = MagicMock()
        mock_cv2.findContours.return_value = ([contour], None)

        # Threshold: 5000 * 0.5^2 = 1250.
        # Let's return area 2000 (should pass)
        mock_cv2.contourArea.return_value = 2000

        # Moments
        # Let's say center is at (100, 100) in small image (320x240)
        # m10/m00 = x, m01/m00 = y
        moments = {"m00": 1, "m10": 100, "m01": 100}
        mock_cv2.moments.return_value = moments

        # Reset mocks to clear previous calls
        mock_cv2.circle.reset_mock()

        # Call detect_gesture
        detector.detect_gesture(frame, draw_landmarks=True)

        # Verify scaling back to original coordinates
        # Input (100, 100) scaled by 1/0.5 = 2.
        # Expected: (200, 200)

        # cv2.circle(frame, (cx, cy), ...)
        # Check call args
        circle_calls = mock_cv2.circle.call_args_list

        # Verify we called circle
        self.assertTrue(len(circle_calls) > 0, "cv2.circle should have been called")

        args, _ = circle_calls[-1]
        # args[0] is frame, args[1] is center (tuple)
        center = args[1]
        self.assertEqual(center, (200, 200))

    def test_threshold_scaling(self):
        # Verify that small contours (below scaled threshold) are ignored
        detector = GestureDetector(processing_scale=0.5)
        frame = MagicMock()
        frame.shape = (480, 640, 3)

        # First call
        detector.detect_gesture(frame)

        # Second call
        contour = MagicMock()
        mock_cv2.findContours.return_value = ([contour], None)

        # Threshold: 5000 * 0.5^2 = 1250.
        # Return area 1000 (should be ignored)
        mock_cv2.contourArea.return_value = 1000

        mock_cv2.circle.reset_mock()
        detector.detect_gesture(frame, draw_landmarks=True)

        # Verify circle NOT called (contour ignored)
        self.assertFalse(mock_cv2.circle.called, "Should verify contour area threshold")

    def test_find_contours_no_copy(self):
        detector = GestureDetector(processing_scale=0.5)
        frame = MagicMock()
        frame.shape = (480, 640, 3)

        # Call 1: Set prev_frame
        detector.detect_gesture(frame, draw_landmarks=False)

        # Call 2: Trigger findContours logic
        mock_thresh = MagicMock()
        # cv2.dilate returns the thresh variable passed to findContours
        mock_cv2.dilate.return_value = mock_thresh

        detector.detect_gesture(frame, draw_landmarks=False)

        # Verify copy was NOT called on thresh
        self.assertFalse(mock_thresh.copy.called, "Should not call .copy() on thresh before findContours")

    def test_inplace_threshold_and_dilate(self):
        detector = GestureDetector(processing_scale=0.5)
        frame = MagicMock()
        frame.shape = (480, 640, 3)

        # First call to initialize prev_frame
        detector.detect_gesture(frame, draw_landmarks=False)

        # Reset mocks to track the second call cleanly
        mock_cv2.threshold.reset_mock()
        mock_cv2.dilate.reset_mock()
        mock_cv2.absdiff.reset_mock()

        # Second call to trigger difference computation
        detector.detect_gesture(frame, draw_landmarks=False)

        # Verify absdiff was called
        self.assertTrue(mock_cv2.absdiff.called, "absdiff should be called to compute frame difference")

        # Get the return value of absdiff, which is frame_delta
        frame_delta = mock_cv2.absdiff.return_value

        # Verify threshold was called with dst=frame_delta
        mock_cv2.threshold.assert_called_with(frame_delta, 25, 255, mock_cv2.THRESH_BINARY, dst=frame_delta)

        # Verify dilate was called with dst=frame_delta
        mock_cv2.dilate.assert_called_with(frame_delta, None, iterations=2, dst=frame_delta)

if __name__ == '__main__':
    unittest.main()
