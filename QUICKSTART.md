# Quick Start Guide

## 5-Minute Setup

### 1. Install (Windows)

```powershell
# Clone repository
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools

# Run automatic installer
powershell -ExecutionPolicy Bypass -File install.ps1
```

### 2. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Run Calibration (First Time Only)

```powershell
python main.py --calibrate
```

### 4. Start Application

```powershell
python main.py
```

---

## First Time Use

### Testing Gestures

1. **Start the application**
   ```powershell
   python main.py
   ```

2. **Position yourself**
   - Stand 1-2 meters from camera
   - Ensure good lighting
   - Face the camera

3. **Test each gesture:**
   - 👉 **Swipe Right** - Move hand dari kiri ke kanan dengan telapak terbuka
   - 👈 **Swipe Left** - Move hand dari kanan ke kiri
   - ✋ **Open Palm** - Tangan terbuka menghadap camera
   - ✊ **Closed Fist** - Kepal tangan
   - 👍 **Thumbs Up** - Jempol ke atas, jari lain tertutup
   - 👎 **Thumbs Down** - Jempol ke bawah
   - ✌️ **Peace Sign** - Dua jari (telunjuk & tengah) terangkat

4. **Watch the screen** - UI overlay akan menampilkan gesture yang terdeteksi

### Testing Voice Commands

1. **Switch to Voice Mode**
   - Tekan **V** pada keyboard

2. **Test commands** (speak clearly):
   - "**next**" atau "**lanjut**" - Next slide
   - "**previous**" atau "**kembali**" - Previous slide
   - "**first**" atau "**pertama**" - First slide
   - "**last**" atau "**terakhir**" - Last slide

3. **Check UI** - Command yang terdeteksi akan muncul di screen

### Using with PowerPoint

1. **Open your presentation** in PowerPoint

2. **Start the tool**
   ```powershell
   python main.py
   ```

3. **Press F5** in PowerPoint (or use voice: "start") to begin presentation

4. **Control with gestures or voice:**
   - Swipe right / say "next" → Next slide
   - Swipe left / say "previous" → Previous slide

5. **Switch modes as needed:**
   - **G** = Gesture only
   - **V** = Voice only
   - **H** = Both (hybrid)

---

## Common Workflows

### Scenario 1: Formal Presentation (Voice Only)

```powershell
# Start application
python main.py

# Press V for voice-only mode
# Open PowerPoint and start presentation (F5)
# Use voice commands: "next", "previous", etc.
```

**Why voice only?**
- More professional (no visible hand gestures)
- Better when standing far from camera
- Less distracting

### Scenario 2: Demo/Workshop (Gesture Only)

```powershell
# Start application
python main.py

# Press G for gesture-only mode
# Open presentation
# Use hand gestures while speaking
```

**Why gesture only?**
- No microphone needed
- Background noise doesn't interfere
- More interactive and engaging

### Scenario 3: Best of Both (Hybrid)

```powershell
# Start application
python main.py

# Press H for hybrid mode (or leave as default)
# Use gestures when convenient
# Use voice when hands are busy
```

**Why hybrid?**
- Maximum flexibility
- Redundancy if one fails
- Natural switching between methods

---

## Tips & Tricks

### 🎯 For Best Gesture Detection

1. **Lighting**: Pastikan wajah dan tangan terlihat jelas
2. **Background**: Simple, kontras dengan warna kulit
3. **Distance**: 0.5 - 2 meter dari camera
4. **Speed**: Gerakan smooth, tidak terlalu cepat
5. **Hold**: Tahan gesture 0.3 detik untuk konfirmasi

### 🎤 For Best Voice Recognition

1. **Clarity**: Speak clearly, tidak terlalu cepat
2. **Volume**: Normal speaking volume
3. **Noise**: Minimize background noise
4. **Distance**: 0.5 - 1 meter dari microphone
5. **Language**: Gunakan satu bahasa konsisten (Indo atau English)

### ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **G** | Switch to Gesture mode |
| **V** | Switch to Voice mode |
| **H** | Switch to Hybrid mode |
| **P** | Pause/Resume detection |
| **A** | Auto-detect application |
| **C** | Run calibration |
| **ESC** | Exit application |

### 📱 Application Profiles

Tool otomatis detect aplikasi yang aktif:

- **PowerPoint** (.pptx, .ppt)
  - F5 = Start presentation
  - Arrow keys = Navigate
  - B = Blackout

- **Google Slides** (Chrome/Edge)
  - Ctrl+F5 = Start presentation
  - Arrow keys = Navigate

- **PDF Viewers** (Adobe, Foxit, etc.)
  - Arrow keys = Navigate
  - Page Up/Down = Navigate

- **Canva Presentation**
  - Arrow keys = Navigate
  - Esc = Exit fullscreen

**Tip**: Tekan **A** untuk force detection ulang jika aplikasi tidak terdeteksi

---

## Troubleshooting Quick Fixes

### Gesture tidak terdeteksi
```powershell
# 1. Check camera
python -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'FAIL')"

# 2. Run calibration
python main.py --calibrate

# 3. Adjust lighting dan posisi
```

### Voice tidak terdeteksi
```powershell
# 1. Test microphone
python main.py --calibrate

# 2. Check Windows settings
# Settings → Privacy → Microphone → Allow

# 3. Reduce background noise
```

### Commands tidak bekerja di presentasi
```powershell
# 1. Ensure presentation window is active (click on it)

# 2. Auto-detect application
# Press A while application is running

# 3. Check application profile
# Different apps use different shortcuts
```

---

## Advanced Configuration

### Custom Gesture Sensitivity

Edit `config.py` atau create `user_config.json`:

```json
{
  "gesture_sensitivity": 0.8,
  "debounce_time": 0.3
}
```

- **Higher sensitivity** = More responsive, but more false positives
- **Lower debounce** = Faster response, but might double-trigger

### Custom Voice Commands

Edit `config.py` → `VOICE_COMMANDS`:

```python
VOICE_COMMANDS = {
    "next": ["next", "lanjut", "maju", "forward"],
    "previous": ["previous", "back", "mundur", "balik"]
}
```

### Disable Sound Effects

```json
{
  "sound_effects": false
}
```

---

## Performance Tips

### If running slow:

1. **Lower camera resolution** (edit `gesture_detector.py`):
   ```python
   self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
   self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
   ```

2. **Use Voice-only mode** when gestures not needed

3. **Disable UI overlay**:
   ```json
   {
     "show_ui": false
   }
   ```

4. **Close other applications** using camera/microphone

---

## Next Steps

1. ✅ Test all gestures before actual presentation
2. ✅ Practice switching between modes
3. ✅ Setup your preferred configuration
4. ✅ Test with your actual presentation file
5. ✅ Have a backup (keyboard/clicker) ready

---

## Quick Reference Card

Print this for quick reference during presentation:

```
┌─────────────────────────────────────────────┐
│   PRESENTATION CONTROL TOOL - QUICK REF     │
├─────────────────────────────────────────────┤
│ GESTURES:                                   │
│  👉 Swipe Right  → Next                     │
│  👈 Swipe Left   → Previous                 │
│  ✋ Open Palm    → Pause                     │
│  👍 Thumbs Up    → First                    │
│  👎 Thumbs Down  → Last                     │
├─────────────────────────────────────────────┤
│ VOICE:                                      │
│  "next" / "lanjut"       → Next            │
│  "previous" / "kembali"  → Previous        │
│  "first" / "pertama"     → First           │
│  "last" / "terakhir"     → Last            │
├─────────────────────────────────────────────┤
│ KEYBOARD:                                   │
│  G = Gesture    V = Voice    H = Hybrid    │
│  P = Pause      A = Detect   ESC = Exit    │
└─────────────────────────────────────────────┘
```

**Happy Presenting! 🎤✨**
