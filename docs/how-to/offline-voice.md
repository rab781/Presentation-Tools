# How-to: Configure Offline Voice Recognition

By default, the Presentation Control Tool relies on Google's Speech-to-Text API. This requires an active internet connection. If you are presenting in a venue with unreliable Wi-Fi, you can configure the tool to use a local Vosk model for offline voice recognition.

This guide shows you how to download, install, and enable the Vosk offline model for Indonesian voice commands.

## Prerequisites

- The Presentation Control Tool installed and functioning.
- Approximately 50MB of free disk space for the offline model.

## Step 1: Create the Models Directory

First, create a directory to store the local AI models. From the root of the Presentation Control Tool project, create a folder named `models`.

```bash
mkdir models
```

## Step 2: Download the Vosk Model

Download the Vosk Indonesian Small Model. This lightweight model provides fast, offline recognition without requiring significant system resources.

[Download Vosk Indonesian Small Model (0.22)](https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip)

## Step 3: Extract the Model

Extract the contents of the downloaded ZIP file directly into the `models` directory you created in Step 1.

The path should look exactly like this:
```
Presentation-Tools/
└── models/
    └── vosk-model-small-id-0.22/
        ├── am/
        ├── conf/
        ├── graph/
        └── ivector/
```

> **Warning**: Ensure you do not have nested folders (e.g., `models/vosk-model-small-id-0.22/vosk-model-small-id-0.22/`). The configuration files must be immediately inside the `vosk-model-small-id-0.22` folder.

## Step 4: Enable Offline Mode

With the model installed, instruct the tool to use it. Open your `user_config.json` file in the project root. If the file does not exist, create it.

Set the `offline_mode` key to `true`.

```json
{
    "offline_mode": true
}
```

## Step 5: Verify Offline Recognition

Start the application to confirm it is using the local model.

```bash
python main.py
```

Look at your terminal output. If the setup is correct, you will see a message indicating that the Vosk model loaded successfully. You can now use Indonesian voice commands (e.g., "lanjut", "kembali") without an internet connection.
