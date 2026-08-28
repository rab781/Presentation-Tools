# How-to: Configure Offline Voice Recognition

By default, the Presentation Control Tool uses Google's speech recognition service, which requires an active internet connection. If you need to present offline or prefer local processing for privacy, you configure the tool to use a local Vosk model.

This guide shows you how to set up the Vosk offline model for Indonesian voice commands.

## Prerequisites

- [x] Presentation Control Tool installed
- [x] Basic familiarity with the command line

## Step 1: Create the Models Directory

First, create a directory to store the local voice model. Run this command from the project root:

```bash
mkdir models
```

## Step 2: Download the Vosk Model

Download the small Indonesian model from the Vosk project. This model provides a good balance between accuracy and performance.

1. Open the [Vosk Indonesian Small Model](https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip) link in your browser to start the download.

## Step 3: Extract the Model

Extract the downloaded ZIP file into the `models` directory you created in Step 1.

Ensure the extracted directory is named exactly `vosk-model-small-id-0.22` and sits directly inside the `models` directory.

Your directory structure looks like this:

```text
Presentation-Tools/
├── main.py
├── config.py
└── models/
    └── vosk-model-small-id-0.22/
        ├── am/
        ├── conf/
        ├── graph/
        └── ivector/
```

## Step 4: Enable Offline Mode

Update your configuration to tell the application to use the offline model.

1. Open or create `user_config.json` in the project root.
2. Set the `offline_mode` property to `true`.

```json
{
  "offline_mode": true
}
```

Alternatively, set this programmatically in your Python script:

```python
from config import config_manager

config_manager.set("offline_mode", True)
```

## Step 5: Verify the Setup

Start the application to ensure it loads the offline model successfully.

```bash
python main.py
```

If the setup is correct, the application starts without internet access and recognizes your Indonesian voice commands. If you see errors about the model not being found, verify your directory structure matches Step 3 exactly.
