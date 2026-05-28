# How-To: Configure Offline Voice Recognition

By default, the Presentation Control Tool uses Google Speech Recognition, which requires an active internet connection. To use voice commands without internet access, you configure the tool to use a local Vosk model.

## Step 1: Create the Models Directory

Create a `models` directory in the root of the project to store the Vosk model.

```bash
mkdir models
```

## Step 2: Download the Vosk Model

Download the Vosk Indonesian Small Model.

- [Download Vosk Indonesian Small Model (0.22)](https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip)

## Step 3: Extract the Model

Extract the contents of the downloaded ZIP file into the `models` directory. Ensure the directory structure looks like this:

```
models/
└── vosk-model-small-id-0.22/
    ├── am/
    ├── conf/
    ├── graph/
    └── ivector/
```

## Step 4: Update the Configuration

Open `user_config.json` in the root of the project (or create it if it does not exist) and set `offline_mode` to `true`.

```json
{
    "offline_mode": true
}
```

Alternatively, you use the API to update the configuration programmatically.

```python
from config import config_manager
config_manager.set("offline_mode", True)
```

## Step 5: Start the Application

Start the application to begin using offline voice recognition.

```bash
python main.py
```
