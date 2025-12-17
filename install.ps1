# Quick Install Script for Windows
# Run this script with: powershell -ExecutionPolicy Bypass -File install.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Presentation Control Tool - Installer" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check Python
Write-Host "[1/6] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found! Please install Python 3.8+" -ForegroundColor Red
    Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment
Write-Host "`n[2/6] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ⚠ Virtual environment already exists, skipping..." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`n[3/6] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Could not activate virtual environment automatically" -ForegroundColor Yellow
    Write-Host "  Please run: .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
}

# Upgrade pip
Write-Host "`n[4/6] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "  ✓ pip upgraded" -ForegroundColor Green

# Install dependencies
Write-Host "`n[5/6] Installing dependencies..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Gray

# Install everything except PyAudio first
Write-Host "  - Installing OpenCV..." -ForegroundColor Gray
pip install opencv-python --quiet
Write-Host "  - Installing MediaPipe..." -ForegroundColor Gray
pip install mediapipe --quiet
Write-Host "  - Installing NumPy..." -ForegroundColor Gray
pip install numpy --quiet
Write-Host "  - Installing PyAutoGUI..." -ForegroundColor Gray
pip install pyautogui --quiet
Write-Host "  - Installing SpeechRecognition..." -ForegroundColor Gray
pip install SpeechRecognition --quiet
Write-Host "  - Installing Pillow..." -ForegroundColor Gray
pip install pillow --quiet
Write-Host "  - Installing PyWin32..." -ForegroundColor Gray
pip install pywin32 --quiet
Write-Host "  - Installing Vosk..." -ForegroundColor Gray
pip install vosk --quiet

# Install PyAudio
Write-Host "  - Installing PyAudio (this might take longer)..." -ForegroundColor Gray
pip install pipwin --quiet
pipwin install pyaudio --quiet 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ All dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "  ⚠ PyAudio installation might have failed" -ForegroundColor Yellow
    Write-Host "  Please install manually from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio" -ForegroundColor Yellow
}

# Test installation
Write-Host "`n[6/6] Testing installation..." -ForegroundColor Yellow
$testScript = @"
import sys
try:
    import cv2
    import mediapipe
    import numpy
    import pyautogui
    import speech_recognition
    import pyaudio
    print('SUCCESS')
except ImportError as e:
    print(f'FAILED: {e}')
    sys.exit(1)
"@

$testResult = python -c $testScript 2>&1
if ($testResult -match "SUCCESS") {
    Write-Host "  ✓ All modules imported successfully!" -ForegroundColor Green
} else {
    Write-Host "  ✗ Some modules failed to import:" -ForegroundColor Red
    Write-Host "    $testResult" -ForegroundColor Red
}

# Optional: Download Vosk model
Write-Host "`n----------------------------------------" -ForegroundColor Cyan
$downloadVosk = Read-Host "Download Vosk model for offline voice recognition? (~50MB) [Y/N]"
if ($downloadVosk -eq "Y" -or $downloadVosk -eq "y") {
    Write-Host "`nDownloading Vosk model..." -ForegroundColor Yellow
    
    if (-not (Test-Path "models")) {
        New-Item -ItemType Directory -Path "models" | Out-Null
    }
    
    $voskUrl = "https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip"
    $voskZip = "models\vosk-model-small-id-0.22.zip"
    
    try {
        Invoke-WebRequest -Uri $voskUrl -OutFile $voskZip
        Write-Host "  ✓ Downloaded Vosk model" -ForegroundColor Green
        
        Write-Host "  Extracting..." -ForegroundColor Gray
        Expand-Archive -Path $voskZip -DestinationPath "models" -Force
        Remove-Item $voskZip
        Write-Host "  ✓ Vosk model installed" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ Failed to download Vosk model" -ForegroundColor Red
        Write-Host "  You can download manually from: $voskUrl" -ForegroundColor Yellow
    }
}

# Final summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Run calibration: python main.py --calibrate" -ForegroundColor White
Write-Host "  2. Start application: python main.py" -ForegroundColor White
Write-Host ""
Write-Host "Controls:" -ForegroundColor Yellow
Write-Host "  G - Gesture only mode" -ForegroundColor White
Write-Host "  V - Voice only mode" -ForegroundColor White
Write-Host "  H - Hybrid mode" -ForegroundColor White
Write-Host "  ESC - Exit" -ForegroundColor White
Write-Host ""
Write-Host "For help, see README.md" -ForegroundColor Gray
Write-Host ""
