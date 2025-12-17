# Installation Guide - Presentation Control Tool

## Windows Installation (Recommended)

### Step 1: Install Python

1. Download Python 3.8+ dari https://www.python.org/downloads/
2. **PENTING**: Centang "Add Python to PATH" saat instalasi
3. Verify instalasi:
```powershell
python --version
```

### Step 2: Clone atau Download Project

**Option A: Using Git**
```powershell
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools
```

**Option B: Download ZIP**
1. Download ZIP dari GitHub
2. Extract ke folder pilihan Anda
3. Buka PowerShell di folder tersebut

### Step 3: Create Virtual Environment (Recommended)

```powershell
# Buat virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Jika error "execution policy", jalankan ini dulu:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Install Dependencies

#### Install semua package kecuali PyAudio
```powershell
pip install opencv-python mediapipe numpy pyautogui SpeechRecognition pillow pywin32 vosk
```

#### Install PyAudio (CRITICAL STEP)

PyAudio adalah dependency yang paling sulit di Windows. Pilih salah satu metode:

**🔹 Method 1: pipwin (Easiest)**
```powershell
pip install pipwin
pipwin install pyaudio
```

**🔹 Method 2: Pre-built Wheel (Most Reliable)**

1. Check Python version dan architecture:
```powershell
python -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor} ({64 if sys.maxsize > 2**32 else 32}-bit)')"
```

2. Download sesuai versi dari: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

Contoh untuk Python 3.11 64-bit:
```powershell
# Download PyAudio-0.2.13-cp311-cp311-win_amd64.whl
# Lalu install:
pip install PyAudio-0.2.13-cp311-cp311-win_amd64.whl
```

**🔹 Method 3: Build dari Source (Advanced)**

Membutuhkan Microsoft C++ Build Tools:
1. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install dengan komponen "Desktop development with C++"
3. Restart komputer
4. Install PyAudio:
```powershell
pip install pyaudio
```

### Step 5: Test Installation

```powershell
# Test semua dependencies
python -c "import cv2, mediapipe, numpy, pyautogui, speech_recognition, pyaudio; print('All dependencies OK!')"
```

### Step 6: Download Vosk Model (Opsional - untuk Offline Mode)

```powershell
# Buat folder models
mkdir models
cd models

# Download model Indonesia (Small - 50MB)
Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip" -OutFile "vosk-model-small-id-0.22.zip"

# Extract
Expand-Archive -Path "vosk-model-small-id-0.22.zip" -DestinationPath "."
Remove-Item "vosk-model-small-id-0.22.zip"

cd ..
```

### Step 7: Run Calibration

```powershell
python main.py --calibrate
```

Calibration akan test:
- ✅ Camera
- ✅ Microphone  
- ✅ Keyboard control
- ✅ Application detection

### Step 8: Run Application

```powershell
python main.py
```

---

## Linux Installation

### Ubuntu/Debian

```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv
sudo apt install portaudio19-dev python3-pyaudio
sudo apt install libopencv-dev python3-opencv

# Clone repository
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Download Vosk model (optional)
mkdir -p models
cd models
wget https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip
unzip vosk-model-small-id-0.22.zip
rm vosk-model-small-id-0.22.zip
cd ..

# Run
python main.py
```

### Arch Linux

```bash
# Install dependencies
sudo pacman -S python python-pip python-virtualenv
sudo pacman -S portaudio python-pyaudio
sudo pacman -S opencv python-opencv

# Rest same as Ubuntu
```

---

## macOS Installation

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python portaudio

# Clone repository
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Run
python main.py
```

---

## Troubleshooting Installation

### "python" command not found

**Windows:**
```powershell
# Try using py instead
py --version
py -m pip install --upgrade pip
```

**Linux/Mac:**
```bash
# Use python3
python3 --version
python3 -m pip install --upgrade pip
```

### PyAudio installation fails

**Error: "Microsoft Visual C++ 14.0 or greater is required"**

Solusi:
1. Download Microsoft C++ Build Tools
2. Atau gunakan pre-built wheel (Method 2 di atas)

**Error: "portaudio.h: No such file or directory"** (Linux)

```bash
sudo apt install portaudio19-dev
```

### ModuleNotFoundError after installation

Pastikan virtual environment aktif:
```powershell
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### Camera not accessible

**Windows:**
- Settings → Privacy → Camera → Allow apps to access camera

**Linux:**
```bash
# Add user to video group
sudo usermod -a -G video $USER
# Logout and login again
```

### Microphone not working

**Windows:**
- Settings → Privacy → Microphone → Allow apps to access microphone

**Linux:**
```bash
# Install PulseAudio
sudo apt install pulseaudio

# Test microphone
arecord -l
```

---

## Verification Checklist

Setelah instalasi, verify semua komponen:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed successfully
- [ ] Camera accessible (test with calibration)
- [ ] Microphone accessible (test with calibration)
- [ ] PyAutoGUI working (test with calibration)
- [ ] Vosk model downloaded (if using offline mode)
- [ ] Application runs without errors

---

## Quick Install Script (Windows)

Save sebagai `install.ps1` dan run:

```powershell
# Quick installation script
Write-Host "Installing Presentation Control Tool..." -ForegroundColor Green

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies (except PyAudio)
pip install opencv-python mediapipe numpy pyautogui SpeechRecognition pillow pywin32 vosk

# Install PyAudio using pipwin
pip install pipwin
pipwin install pyaudio

# Test installation
python -c "import cv2, mediapipe, numpy, pyautogui, speech_recognition, pyaudio; print('Installation successful!')"

Write-Host "Installation complete! Run 'python main.py' to start." -ForegroundColor Green
```

Run dengan:
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

---

## Need Help?

- Run calibration: `python main.py --calibrate`
- Check README.md for usage guide
- Open issue di GitHub
- Check Troubleshooting section

Happy Installing! 🚀
