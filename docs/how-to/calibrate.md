# How-To: Calibrate Your Setup

If you experience issues with gesture detection or voice recognition, run the calibration wizard to test your setup and receive recommended settings.

## Step 1: Run the Calibration Wizard

Start the application with the `--calibrate` flag to launch the calibration wizard.

```bash
python main.py --calibrate
```

Alternatively, press the `C` key while the application is running to trigger the calibration wizard.

## Step 2: Follow the Prompts

The calibration wizard tests the following components:

1. **Camera**: Verifies camera access and resolution.
2. **Microphone**: Tests microphone access and adjusts for ambient noise.
3. **Keyboard Control**: Verifies that PyAutoGUI can simulate keyboard inputs.
4. **Application Detection**: Identifies the currently active presentation software.

Review the output and apply any recommendations provided by the wizard.

## Common Fixes

- **Camera Error**: Ensure no other applications (e.g., Zoom, Teams) are using the camera.
- **Microphone Error**: Check your system's privacy settings to ensure Python has permission to access the microphone.
- **Keyboard Control Error**: On macOS, ensure Python has Accessibility permissions in System Preferences > Security & Privacy.
