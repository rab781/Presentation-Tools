import sys
import unittest
from unittest.mock import MagicMock, patch
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock psutil to avoid errors when importing
mock_psutil = MagicMock()
sys.modules['psutil'] = mock_psutil

# Ensure win32gui and win32process are available as mocks if they aren't installed
try:
    import win32gui
except ImportError:
    mock_win32gui = MagicMock()
    sys.modules['win32gui'] = mock_win32gui

try:
    import win32process
except ImportError:
    mock_win32process = MagicMock()
    sys.modules['win32process'] = mock_win32process

import controller

class TestAppDetectionOptimization(unittest.TestCase):

    @patch.object(controller.win32gui, 'GetForegroundWindow', return_value=12345)
    @patch.object(controller.win32gui, 'GetWindowText')
    @patch.object(controller.psutil, 'Process')
    def test_powerpoint_title_bypasses_psutil(self, mock_process, mock_get_text, mock_get_window):
        mock_get_text.return_value = "My Presentation - PowerPoint"

        c = controller.PresentationController()
        detected = c.detect_active_application()

        self.assertEqual(detected, "powerpoint")
        mock_process.assert_not_called()

    @patch.object(controller.win32gui, 'GetForegroundWindow', return_value=12345)
    @patch.object(controller.win32gui, 'GetWindowText')
    @patch.object(controller.psutil, 'Process')
    def test_google_slides_title_bypasses_psutil(self, mock_process, mock_get_text, mock_get_window):
        mock_get_text.return_value = "Google Slides - Presentation"

        c = controller.PresentationController()
        detected = c.detect_active_application()

        self.assertEqual(detected, "google_slides")
        mock_process.assert_not_called()

    @patch.object(controller.win32gui, 'GetForegroundWindow', return_value=12345)
    @patch.object(controller.win32gui, 'GetWindowText')
    @patch.object(controller.psutil, 'Process')
    def test_canva_title_bypasses_psutil(self, mock_process, mock_get_text, mock_get_window):
        mock_get_text.return_value = "Canva - Presentation"

        c = controller.PresentationController()
        detected = c.detect_active_application()

        self.assertEqual(detected, "canva")
        mock_process.assert_not_called()

    @patch.object(controller.win32gui, 'GetForegroundWindow', return_value=12345)
    @patch.object(controller.win32process, 'GetWindowThreadProcessId', return_value=(0, 67890))
    @patch.object(controller.win32gui, 'GetWindowText')
    @patch.object(controller.psutil, 'Process')
    def test_generic_title_falls_back_to_psutil(self, mock_process, mock_get_text, mock_get_thread, mock_get_window):
        mock_get_text.return_value = "My File - Unknown"

        mock_process_instance = MagicMock()
        mock_process_instance.name.return_value = "powerpnt.exe"
        mock_process.return_value = mock_process_instance

        c = controller.PresentationController()
        detected = c.detect_active_application()

        self.assertEqual(detected, "powerpoint")
        mock_process.assert_called_once_with(67890)

if __name__ == '__main__':
    unittest.main()
