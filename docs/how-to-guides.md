# How-To Guides

This guide contains task-oriented instructions to help you accomplish specific goals with the Presentation Control Tool.

---

## Configure Offline Voice Recognition

By default, the tool uses Google's speech recognition engine, which requires an active internet connection. To use voice commands without internet access, configure the offline Vosk model.

1. Create a `models` directory in the root of your project folder.
   ```bash
   mkdir models
   cd models
   ```

2. Download the [Vosk Indonesian Small Model](https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip) or a compatible English model from the Vosk website.

3. Extract the contents of the `.zip` file into the `models` directory. The extracted folder must be named `vosk-model-small-id-0.22`.

4. Update your `user_config.json` file in the project root to enable offline mode.

   ```json
   {
       "offline_mode": true
   }
   ```

5. Run `python main.py` again. The tool will now load the local model.

## Run the Calibration Wizard

If you experience inconsistent gesture detection or voice recognition, run the built-in calibration wizard. It tests your hardware and provides specific, actionable recommendations to improve tracking.

1. Ensure your camera and microphone are plugged in and not used by another application.

2. Run the main script with the `--calibrate` flag.

   ```bash
   python main.py --calibrate
   ```

3. Follow the on-screen prompts. The wizard will test your camera resolution, adjust your microphone for ambient noise, verify that keyboard simulation is working, and attempt to auto-detect your currently active application.

4. Review the final recommendations, such as adjusting your lighting or distance from the camera.

## Use Keyboard Controls

While the application is running, you can press specific keys on your keyboard to control the tool's behavior without editing configuration files. The camera window must be focused to receive these keystrokes.

- **Mode Switching**: Press `G` to switch to Gesture Only mode, `V` for Voice Only mode, or `H` for Hybrid mode.
- **Auto-Detect**: Press `A` to have the tool search for an open presentation application (like PowerPoint or a browser window).
- **Manual Select**: Press `S` to manually choose a presentation software profile.
- **Pause Detection**: Press `P` to pause or resume gesture and voice tracking. This prevents accidental triggers while you are talking or moving but not presenting.
- **Exit**: Press `ESC` to close the application safely.