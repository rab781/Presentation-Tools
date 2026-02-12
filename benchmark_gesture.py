
import sys
import time
import unittest.mock
from unittest.mock import MagicMock

# Mock dependencies if not present
try:
    import cv2
    import numpy as np
except ImportError:
    # Mock numpy
    mock_np = MagicMock()
    sys.modules["numpy"] = mock_np

    # Mock cv2
    mock_cv2 = MagicMock()
    sys.modules["cv2"] = mock_cv2

    # Setup mock behavior to simulate processing time
    def mock_resize(src, dsize):
        m = MagicMock()
        m.shape = (dsize[1], dsize[0])
        m.size = dsize[0] * dsize[1]
        time.sleep(m.size * 1e-7) # Simulate processing time proportional to pixels
        return m

    def mock_cvtColor(src, code):
        m = MagicMock()
        if hasattr(src, 'shape'):
            m.shape = src.shape[:2]
            m.size = src.shape[0] * src.shape[1]
        else:
            m.shape = (480, 640)
            m.size = 640 * 480
        time.sleep(m.size * 1e-7)
        return m

    def mock_GaussianBlur(src, ksize, sigmaX):
        time.sleep(src.size * 5e-7) # Blur is expensive
        return src

    def mock_absdiff(src1, src2):
        time.sleep(src1.size * 1e-7)
        return src1

    def mock_threshold(src, thresh, maxval, type):
        time.sleep(src.size * 1e-7)
        return (0, src)

    def mock_findContours(image, mode, method):
        # Return empty contours
        return [], None

    def mock_flip(src, flipCode):
        return src

    def mock_putText(img, text, org, fontFace, fontScale, color, thickness):
        pass

    def mock_circle(img, center, radius, color, thickness):
        pass

    def mock_drawContours(image, contours, contourIdx, color, thickness):
        pass

    mock_cv2.resize.side_effect = mock_resize
    mock_cv2.cvtColor.side_effect = mock_cvtColor
    mock_cv2.GaussianBlur.side_effect = mock_GaussianBlur
    mock_cv2.absdiff.side_effect = mock_absdiff
    mock_cv2.threshold.side_effect = mock_threshold
    mock_cv2.findContours.side_effect = mock_findContours
    mock_cv2.flip.side_effect = mock_flip
    mock_cv2.putText.side_effect = mock_putText
    mock_cv2.circle.side_effect = mock_circle
    mock_cv2.drawContours.side_effect = mock_drawContours

    # Constants
    mock_cv2.COLOR_BGR2GRAY = 6
    mock_cv2.THRESH_BINARY = 0
    mock_cv2.RETR_EXTERNAL = 0
    mock_cv2.CHAIN_APPROX_SIMPLE = 2
    mock_cv2.FONT_HERSHEY_SIMPLEX = 0


# Now import the module to test
# We need to add current directory to path so import works
import os
sys.path.append(os.getcwd())

try:
    from gesture_detector import GestureDetector
except ImportError as e:
    print(f"Failed to import gesture_detector: {e}")
    sys.exit(1)

def benchmark():
    print("="*60)
    print("BENCHMARKING GESTURE DETECTOR")
    print("="*60)

    # Create a fake frame
    frame = MagicMock()
    frame.shape = (480, 640, 3)
    frame.size = 640 * 480 * 3

    # Test with default settings (full resolution)
    try:
        # Explicitly set processing_scale=1.0 for baseline
        detector = GestureDetector(processing_scale=1.0)
    except Exception as e:
        print(f"Failed to instantiate GestureDetector: {e}")
        return

    print("\nRunning baseline (full resolution)...")

    start_time = time.time()
    iterations = 100

    for _ in range(iterations):
        detector.detect_gesture(frame, draw_landmarks=False)

    duration = time.time() - start_time
    fps = iterations / duration
    print(f"Baseline: {duration:.4f}s for {iterations} frames")
    print(f"FPS: {fps:.2f}")

    # Test with optimization (if implemented)
    import inspect
    sig = inspect.signature(GestureDetector.__init__)
    if 'processing_scale' in sig.parameters:
        print("\nRunning optimized (half resolution)...")
        detector_opt = GestureDetector(processing_scale=0.5)

        start_time = time.time()
        for _ in range(iterations):
            detector_opt.detect_gesture(frame, draw_landmarks=False)

        duration_opt = time.time() - start_time
        fps_opt = iterations / duration_opt
        print(f"Optimized: {duration_opt:.4f}s for {iterations} frames")
        print(f"FPS: {fps_opt:.2f}")

        speedup = duration / duration_opt if duration_opt > 0 else 0
        print(f"\nSpeedup: {speedup:.2f}x")
    else:
        print("\nOptimization not yet implemented.")

if __name__ == "__main__":
    benchmark()
