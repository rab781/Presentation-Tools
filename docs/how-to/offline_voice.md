# How to Configure Offline Voice Recognition

This guide explains how to configure the Presentation Control Tool to use offline voice recognition using Vosk. Offline mode is useful for presenting in environments with unstable internet connections or for privacy reasons.

Currently, the tool supports an offline Vosk model for Indonesian commands.

## Step 1: Install the Vosk Library

First, ensure you have the Vosk library installed.

```bash
pip install vosk
```

## Step 2: Download the Vosk Model

Download the Vosk Indonesian Small Model.

1.  Create a `models` directory in the project root:
    ```bash
    mkdir models
    ```
2.  Download the model from the Vosk website:
    [Vosk Indonesian Small Model](https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip)
3.  Extract the downloaded ZIP file into the `models` directory. The extracted folder should be named `vosk-model-small-id-0.22`.

The final structure should look like this:
```
Presentation-Tools/
└── models/
    └── vosk-model-small-id-0.22/
        ├── am/
        ├── conf/
        ├── graph/
        └── ivector/
```

## Step 3: Enable Offline Mode

Update your `user_config.json` file in the project root to enable offline mode. If the file doesn't exist, you can create it.

```json
{
  "offline_mode": true,
  "language": "indonesian"
}
```

Alternatively, you can set this programmatically using the API:

```python
from config import config_manager

config_manager.set("offline_mode", True)
config_manager.set("language", "indonesian")
```

## Step 4: Verify Offline Mode

Run the application as normal.

```bash
python main.py
```

When you speak a command (e.g., "lanjut", "kembali"), the application should recognize it locally without sending data to Google's servers. You can test this by disconnecting from the internet and verifying that voice commands still work.
