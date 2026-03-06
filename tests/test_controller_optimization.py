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

if __name__ == '__main__':
    unittest.main()
