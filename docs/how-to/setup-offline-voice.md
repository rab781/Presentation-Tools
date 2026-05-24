# How to Set Up Offline Voice Recognition

By default, the voice recognition module relies on Google's cloud services. For privacy, low-latency performance, or environments without internet access, you configure the tool to use a local Vosk model for offline speech recognition in Indonesian.

## Prerequisites

- [ ] A working Python environment with dependencies installed
- [ ] At least 100MB of free disk space

---

## Step 1: Create the Models Directory

First, create a `models` directory in the root of the project.

```bash
mkdir models
```

## Step 2: Download the Vosk Model

Download the Vosk Indonesian Small Model. This model provides a good balance between accuracy and performance for voice commands.

[Download Vosk Indonesian Small Model](https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip)

## Step 3: Extract the Model

Extract the downloaded ZIP file into the `models` directory you just created. Ensure the final path is `models/vosk-model-small-id-0.22/` rather than nested an extra level deep.

## Step 4: Update Configuration

You enable offline mode by changing the configuration. Edit your `user_config.json` (or use the application's configuration tool) to set the `offline_mode` value to `true`.

```json
{
  "offline_mode": true
}
```

The application now uses the local Vosk model instead of the cloud service for voice recognition.
