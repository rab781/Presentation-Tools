import sys
import unittest
from unittest.mock import MagicMock, patch
import os
import time

# Mock external dependencies
sys.modules['pyautogui'] = MagicMock()
mock_winsound = MagicMock()
sys.modules['winsound'] = mock_winsound

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from controller import PresentationController
except ImportError as e:
    print(f"Could not import PresentationController: {e}")
    sys.exit(1)

class TestControllerOptimization(unittest.TestCase):

    @patch('winsound.Beep', create=True)
    def test_play_sound_effect_non_blocking(self, mock_beep):
        # Setup mock Beep to simulate a blocking call (e.g., 100ms delay)
        def mock_blocking_beep(frequency, duration):
            time.sleep(0.1) # Simulate the 100ms blocking

        mock_beep.side_effect = mock_blocking_beep

        # Instantiate controller
        controller = PresentationController()

        # Enable sound to ensure the code path is hit
        controller.sound_enabled = True

        # Call _play_sound_effect and measure time
        start_time = time.time()
        controller._play_sound_effect("next")
        end_time = time.time()

        duration = end_time - start_time

        # Wait slightly to let the background thread run the mock and register the call
        time.sleep(0.15)

        # Verify that the main thread wasn't blocked
        # It should take significantly less than the 100ms simulated blocking time
        self.assertLess(duration, 0.05, "The main thread was blocked by _play_sound_effect.")

        # Verify the beep was actually called in the background
        mock_beep.assert_called_once_with(800, 100)

    @patch('controller.HAS_WIN32', True)
    @patch('controller.win32gui', create=True)
    @patch('controller.win32process', create=True)
    @patch('controller.psutil', create=True)
    def test_detect_active_application_caching(self, mock_psutil, mock_win32process, mock_win32gui):
        import controller

        # Setup mocks
        mock_win32gui.GetForegroundWindow.return_value = 12345
        mock_win32gui.GetWindowText.return_value = "Google Slides - Google Chrome"
        mock_win32process.GetWindowThreadProcessId.return_value = (0, 9999)
        mock_process = MagicMock()
        mock_process.name.return_value = "chrome.exe"
        mock_psutil.Process.return_value = mock_process

        c = controller.PresentationController()

        # First call should hit psutil
        c.detect_active_application()
        mock_psutil.Process.assert_called_once_with(9999)
        mock_process.name.assert_called_once()

        # Reset mock
        mock_psutil.Process.reset_mock()
        mock_process.name.reset_mock()

        # Second call with same window should use cache
        c.detect_active_application()
        mock_psutil.Process.assert_not_called()
        mock_process.name.assert_not_called()

        # Third call with new window should hit psutil again
        mock_win32gui.GetForegroundWindow.return_value = 54321
        mock_win32gui.GetWindowText.return_value = "PowerPoint"
        mock_win32process.GetWindowThreadProcessId.return_value = (0, 8888)
        mock_process2 = MagicMock()
        mock_process2.name.return_value = "powerpnt.exe"
        mock_psutil.Process.return_value = mock_process2

        c.detect_active_application()
        mock_psutil.Process.assert_called_once_with(8888)
        mock_process2.name.assert_called_once()

if __name__ == '__main__':
    unittest.main()
