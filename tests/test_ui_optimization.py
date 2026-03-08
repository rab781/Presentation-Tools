import sys
import unittest
from unittest.mock import MagicMock
import os

mock_cv2 = MagicMock()
sys.modules['cv2'] = mock_cv2
mock_np = MagicMock()
sys.modules['numpy'] = mock_np
sys.modules['pyaudio'] = MagicMock()
sys.modules['speech_recognition'] = MagicMock()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from main import PresentationToolApp
except ImportError as e:
    print(f"Could not import main: {e}")
    sys.exit(1)

class TestUIOptimization(unittest.TestCase):
    def test_draw_ui_no_full_frame_copy(self):
        app = PresentationToolApp()
        app.show_ui = True

        # Create a mock frame that looks like a numpy array
        mock_frame = MagicMock()
        mock_frame.shape = (480, 640, 3)
        mock_frame.copy.return_value = MagicMock()

        # Call _draw_ui
        result = app._draw_ui(mock_frame)

        # Assert copy was NOT called on the full frame for the overlay
        # Because our optimization uses array slicing `frame[0:120, 0:w]` instead
        self.assertFalse(mock_frame.copy.called, "The full frame should not be copied for the UI overlay")

        # Note: _draw_ui uses array slicing, which on a MagicMock translates to a __getitem__ call
        # And np.zeros_like was called
        mock_np.zeros_like.assert_called()
        mock_cv2.addWeighted.assert_called()

if __name__ == '__main__':
    unittest.main()
