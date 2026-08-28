# How-To: Configure Offline Voice Recognition

By default, the Presentation Control tool uses Google Speech Recognition, which requires an active internet connection. If you need to present in environments with unreliable internet or want faster local processing, you configure the tool to use Vosk for offline voice recognition.

## Step 1: Download the Offline Model

The tool is configured by default to use the Vosk Indonesian small model (`vosk-model-small-id-0.22`), but you can download others if needed.

1. Download the [Vosk Indonesian Small Model](https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip) or another model of your choice from the [Vosk Models page](https://alphacephei.com/vosk/models).
2. Create a `models` directory in the root of the project.
3. Extract the contents of the `.zip` file into the `models` directory. The extracted folder should be named `vosk-model-small-id-0.22`.

## Step 2: Enable Offline Mode

Use the configuration API to enable offline mode and specify your language. This configuration will persist in your `user_config.json` automatically.

Create a new Python script (e.g., `enable_offline.py`) in the project directory:

```python
from config import config_manager

# Enable offline mode using Vosk
config_manager.set("offline_mode", True)

# Set the active language (e.g., "indonesian", "english", or "both")
config_manager.set("language", "indonesian")

print("Offline mode enabled successfully.")
```

Run the script:

```bash
python enable_offline.py
```

## Step 3: Run the Application

Start the main application as usual.

```bash
python main.py
```

When you speak voice commands, the application will now process the audio locally using the Vosk model instead of sending requests to the Google API. This ensures low latency and offline availability.