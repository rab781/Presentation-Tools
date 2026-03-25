# How-To Guides

This guide covers specific tasks for operating and configuring the Presentation Control Tool.

## Change Operation Modes

You can switch the tool between gesture-only, voice-only, or hybrid mode while it is running. The active mode is displayed in the UI.

1. Run the application (`python main.py`).
2. Make sure the Presentation Controller window is active.
3. Press **`G`** to switch to Gesture-Only mode. Voice recognition will stop.
4. Press **`V`** to switch to Voice-Only mode. The camera will stop detecting gestures, but the UI will remain if enabled.
5. Press **`H`** to return to Hybrid mode (default), which enables both.

## Run the Calibration Wizard

If you are having trouble with gesture tracking or voice recognition, run the calibration wizard to test your hardware and environmental conditions.

1. Open your terminal in the project directory.
2. Run the application with the `--calibrate` flag:
   ```bash
   python main.py --calibrate
   ```
3. Follow the prompts in the console. The wizard will test your camera resolution, microphone sensitivity, PyAutoGUI setup, and active application detection.
4. Note the recommendations provided at the end of the wizard (e.g., lighting, distance, background noise).

## Manually Select an Application Profile

By default, the tool automatically detects if you are using PowerPoint, Google Slides, a PDF viewer, or Canva. If auto-detection fails, you can force it to use a specific profile.

1. Run the application (`python main.py`).
2. Make sure the Presentation Controller window is active.
3. Press **`S`** to open the selection menu in your terminal.
4. Type the corresponding number for your application (e.g., `1` for PowerPoint, `2` for Google Slides) or `A` to retry auto-detection.
5. Alternatively, you can use hotkeys directly from the active window:
   - **`1`**: PowerPoint
   - **`2`**: Google Slides
   - **`3`**: PDF Viewer
   - **`4`**: Canva
   - **`5`**: Universal (works with any app)

## Enable Offline Voice Recognition

You can use a local Vosk model to recognize Indonesian commands without an internet connection.

1. Create a `models` directory in the root of your project.
2. Download the [Vosk Indonesian Small Model](https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip).
3. Extract the contents so the path matches `./models/vosk-model-small-id-0.22`.
4. Open (or create) `user_config.json` in the project root.
5. Set `"offline_mode": true`.
6. Restart the application. You will see "Vosk model loaded" in the console output.
