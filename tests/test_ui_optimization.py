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
    def test_ui_dimming_uses_bitwise_shift(self, mock_controller):
        # Initialize app
        app = PresentationToolApp()

        # Create a mock frame
        frame = MagicMock()
        frame.shape = (480, 640, 3)

        # Configure the slice view behavior
        mock_roi = MagicMock()
        frame.__getitem__.return_value = mock_roi
        # The slice view receives the in-place shift operation
        mock_roi.__irshift__.return_value = mock_roi

        # Call draw UI
        app._draw_ui(frame)

        # Verify addWeighted is NOT used
        mock_cv2.addWeighted.assert_not_called()

        # Verify slice was accessed
        frame.__getitem__.assert_called()

        # Verify in-place shift was applied to the slice
        mock_roi.__irshift__.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
