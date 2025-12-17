# Troubleshooting Guide

## Common Issues and Solutions

### 🎥 Camera Issues

#### Issue: Camera not detected / "Cannot open camera"

**Solution 1: Check Windows Privacy Settings**
```
1. Open Windows Settings
2. Privacy → Camera
3. Enable "Allow apps to access your camera"
4. Enable for Python specifically
```

**Solution 2: Check if camera is in use**
```powershell
# Close any apps using camera (Zoom, Teams, Skype, etc.)
# Then test:
python -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'FAIL')"
```

**Solution 3: Try different camera index**
Edit `config.py` or `user_config.json`:
```json
{
  "camera_index": 1
}
```

**Solution 4: Update camera drivers**
```
1. Open Device Manager
2. Imaging devices → Right-click camera
3. Update driver
4. Restart computer
```

---

### 🎤 Microphone Issues

#### Issue: Voice commands not recognized

**Solution 1: Check microphone permissions**
```
1. Windows Settings → Privacy → Microphone
2. Enable "Allow apps to access your microphone"
```

**Solution 2: Test microphone**
```powershell
python main.py --calibrate
# Check if microphone energy threshold is reasonable (3000-5000)
```

**Solution 3: Adjust energy threshold**
Edit `config.py`:
```python
VOICE_CONFIG = {
    "energy_threshold": 3000,  # Lower for quiet environments
    "dynamic_energy": True
}
```

**Solution 4: Reduce background noise**
- Close windows
- Turn off fans/AC
- Move to quieter location
- Use headset microphone

**Solution 5: Speak more clearly**
- Speak at normal volume
- Enunciate clearly
- Don't speak too fast
- Use consistent language (Indo or English)

#### Issue: "PyAudio not found" error

See [Installation Issues](#-installation-issues) below.

---

### ⌨️ Keyboard Control Issues

#### Issue: Commands not controlling presentation

**Solution 1: Ensure presentation window is active**
```
1. Click on presentation window
2. Make sure it has focus (title bar is colored)
3. Try command again
```

**Solution 2: Auto-detect application**
```
1. Open your presentation app
2. Start presentation tool
3. Press 'A' key to auto-detect
```

**Solution 3: Manually set application**
Edit `main.py` or add to controller:
```python
controller.set_application("powerpoint")  # or "google_slides", "pdf_viewer", etc.
```

**Solution 4: Check if app requires admin privileges**
```powershell
# Run as administrator
# Right-click PowerShell → Run as Administrator
cd "path\to\Presentation Tools"
python main.py
```

**Solution 5: Test keyboard control**
```powershell
python -c "import pyautogui; pyautogui.press('right'); print('Key pressed')"
```

---

### 👋 Gesture Detection Issues

#### Issue: Gestures not detected

**Solution 1: Check lighting**
- Increase room lighting
- Avoid backlighting (light behind you)
- Face toward light source
- Use natural or white light

**Solution 2: Check distance**
- Optimal: 0.5 - 2 meters from camera
- Too close: Hand too large
- Too far: Hand too small

**Solution 3: Check background**
- Use solid, contrasting background
- Avoid busy patterns
- Ensure hand is visible against background

**Solution 4: Adjust sensitivity**
Edit `config.py` or `user_config.json`:
```json
{
  "gesture_sensitivity": 0.8
}
```

Edit `config.py` GESTURE_CONFIG:
```python
GESTURE_CONFIG = {
    "min_detection_confidence": 0.6,  # Lower = more sensitive
    "swipe_threshold": 0.10  # Lower = shorter swipe needed
}
```

**Solution 5: Perform gestures correctly**
- Hold gesture for 0.3 seconds
- Make clear, deliberate movements
- Keep hand fully visible
- Swipe with open palm

#### Issue: Too many false positives

**Solution: Increase debouncing**
```json
{
  "debounce_time": 1.0,
  "gesture_sensitivity": 0.5
}
```

---

### 💻 Installation Issues

#### Issue: PyAudio installation fails

**Error: "Microsoft Visual C++ 14.0 or greater is required"**

**Solution 1: Use pipwin (Easiest)**
```powershell
pip install pipwin
pipwin install pyaudio
```

**Solution 2: Download pre-built wheel**
```powershell
# 1. Check your Python version
python -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor} ({64 if sys.maxsize > 2**32 else 32}-bit)')"

# 2. Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
#    Example: PyAudio-0.2.13-cp311-cp311-win_amd64.whl

# 3. Install
pip install PyAudio-0.2.13-cp311-cp311-win_amd64.whl
```

**Solution 3: Install Build Tools**
```
1. Download Microsoft C++ Build Tools
   https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install with "Desktop development with C++"
3. Restart computer
4. pip install pyaudio
```

#### Issue: "No module named 'mediapipe'"

```powershell
pip install mediapipe
```

#### Issue: Import errors after installation

**Solution 1: Check virtual environment**
```powershell
# Make sure venv is activated
.\venv\Scripts\Activate.ps1

# Verify
python -c "import sys; print(sys.prefix)"
# Should show path to venv folder
```

**Solution 2: Reinstall in venv**
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### Issue: "pip" command not found

```powershell
# Use this instead:
python -m pip install -r requirements.txt
```

---

### 🚀 Performance Issues

#### Issue: High CPU usage / Slow performance

**Solution 1: Use voice-only mode**
```
Press 'V' when app is running
```

**Solution 2: Reduce camera resolution**
Edit `gesture_detector.py`:
```python
self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
```

**Solution 3: Disable UI overlay**
```json
{
  "show_ui": false
}
```

**Solution 4: Reduce camera FPS**
Edit `gesture_detector.py`:
```python
self.cap.set(cv2.CAP_PROP_FPS, 15)  # Lower FPS
```

**Solution 5: Close other applications**
- Close browser tabs
- Close other camera/microphone apps
- Close unnecessary background apps

#### Issue: Laggy video feed

**Solution: Skip frames**
Edit `gesture_detector.py`, add to detect_gesture:
```python
# Process every other frame
if self.frame_count % 2 == 0:
    return None, frame
```

---

### 🔧 Configuration Issues

#### Issue: Settings not saving

**Solution 1: Check permissions**
```powershell
# Ensure you can write to folder
New-Item -ItemType File -Path "user_config.json" -Force
```

**Solution 2: Manually create config**
Create `user_config.json`:
```json
{
  "mode": "hybrid",
  "gesture_sensitivity": 0.7,
  "voice_sensitivity": 0.6,
  "debounce_time": 0.5,
  "camera_index": 0,
  "show_ui": true,
  "sound_effects": true,
  "offline_mode": false
}
```

#### Issue: Config changes not taking effect

**Solution: Delete config and restart**
```powershell
Remove-Item user_config.json
python main.py
```

---

### 🌐 Voice Recognition Issues

#### Issue: Only recognizes English, not Indonesian

**Solution 1: Check language setting**
```json
{
  "language": "both"
}
```

**Solution 2: Ensure Vosk model is installed**
```powershell
# Download Indonesian model
mkdir models -Force
cd models
Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip" -OutFile "vosk-model.zip"
Expand-Archive -Path "vosk-model.zip" -DestinationPath "."
cd ..
```

**Solution 3: Test specific commands**
```
Say exactly: "lanjut" (not "lanjutkan" or "selanjutnya")
```

#### Issue: Internet connection required

**Solution: Use offline mode**
```json
{
  "offline_mode": true
}
```

Then install Vosk model (see above).

---

### 🎯 Application-Specific Issues

#### Issue: Not working with PowerPoint

**Solution 1: Start presentation mode first**
```
1. Open PowerPoint
2. Press F5 to start presentation
3. Use gestures/voice
```

**Solution 2: Check PowerPoint shortcuts**
```
Right Arrow = Next (should work)
Left Arrow = Previous (should work)
```

**Solution 3: Force PowerPoint profile**
```python
# In main.py, after controller initialization:
controller.set_application("powerpoint")
```

#### Issue: Not working with Google Slides

**Solution: Ensure browser is in focus**
```
1. Open Google Slides in browser
2. Start presentation (Ctrl+F5 or Present button)
3. Click on presentation window
4. Use gestures/voice
```

#### Issue: Not working with PDF

**Solution: Most PDF viewers support arrow keys**
```
Ensure PDF is in fullscreen/presentation mode
Press F5 in most PDF viewers
```

---

### 🐛 Error Messages

#### Error: "RuntimeError: Cannot open camera 0"

See [Camera Issues](#-camera-issues)

#### Error: "OSError: [Errno -9996] Invalid input device"

See [Microphone Issues](#-microphone-issues)

#### Error: "ModuleNotFoundError: No module named 'X'"

```powershell
# Activate venv first
.\venv\Scripts\Activate.ps1

# Then install missing module
pip install X
```

#### Error: "PyAutoGUI fail-safe triggered"

```
Don't move mouse to top-left corner quickly
Or edit main.py to disable:
pyautogui.FAILSAFE = False
```

#### Error: "cv2.error: OpenCV(4.x.x) error"

```powershell
# Reinstall OpenCV
pip uninstall opencv-python
pip install opencv-python
```

---

## 🔍 Diagnostic Commands

### Full System Check
```powershell
python test_setup.py
```

### Check Python Version
```powershell
python --version
```

### Check Installed Packages
```powershell
pip list
```

### Test Individual Components

**Test Camera:**
```powershell
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera:', 'OK' if cap.isOpened() else 'FAIL'); cap.release()"
```

**Test Microphone:**
```powershell
python -c "import speech_recognition as sr; r = sr.Recognizer(); m = sr.Microphone(); print('Mic: OK')"
```

**Test MediaPipe:**
```powershell
python -c "import mediapipe as mp; print('MediaPipe:', mp.__version__)"
```

**Test PyAutoGUI:**
```powershell
python -c "import pyautogui; print('PyAutoGUI:', pyautogui.size())"
```

---

## 🆘 Still Having Issues?

### 1. Run Full Diagnostic
```powershell
python test_setup.py > diagnostic.txt 2>&1
```

### 2. Run Calibration
```powershell
python main.py --calibrate
```

### 3. Check Logs
Look for error messages in terminal output

### 4. Try Minimal Setup
```powershell
# Test with voice only
python main.py
# Press 'V' immediately
```

### 5. Get Help

Create GitHub issue with:
- OS version (Windows 10/11)
- Python version
- Output from `python test_setup.py`
- Error messages
- Steps to reproduce

---

## 📚 Additional Resources

- **README.md** - Full documentation
- **INSTALL.md** - Installation guide
- **QUICKSTART.md** - Quick start guide
- **GitHub Issues** - Known issues and solutions

---

**Remember**: Most issues are related to:
1. Camera/microphone permissions
2. PyAudio installation
3. Application window focus
4. Lighting conditions

Check these first! 🎯
