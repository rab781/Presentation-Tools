import sys
import unittest
from unittest.mock import MagicMock, patch
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
mock_cv2.FONT_HERSHEY_SIMPLEX = 0
mock_cv2.addWeighted.return_value = MagicMock()

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from main import PresentationToolApp
except ImportError as e:
    print(f"Could not import PresentationToolApp: {e}")
    sys.exit(1)

class TestUIOptimization(unittest.TestCase):
    def setUp(self):
        # Reset mocks
        mock_cv2.reset_mock()

    @patch('main.PresentationController')
    def test_add_weighted_uses_dst(self, mock_controller):
        # Initialize app
        app = PresentationToolApp()

        # Create a mock frame
        frame = MagicMock()
        frame.shape = (480, 640, 3)

        # Call draw UI
        app._draw_ui(frame)

        # Verify addWeighted was called with dst
        mock_cv2.addWeighted.assert_called_once()

        # Get kwargs from the call
        kwargs = mock_cv2.addWeighted.call_args[1]

        self.assertIn('dst', kwargs, "cv2.addWeighted should be called with 'dst' parameter for in-place optimization")

if __name__ == '__main__':
    unittest.main()
