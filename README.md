# Presentation Control Tool

Alat kontrol presentasi menggunakan **gerakan tangan** dan **perintah suara** untuk mengontrol slide PowerPoint, Google Slides, Canva, PDF, dan aplikasi presentasi lainnya.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10%2B-orange)

## ✨ Fitur

- 🖐️ **Deteksi Gerakan Tangan** - Gunakan gerakan tangan untuk navigasi slide
- 🎤 **Perintah Suara** - Kontrol presentasi dengan suara (Indonesia & English)
- 🔄 **3 Mode Operasi** - Gesture only, Voice only, atau Hybrid
- 🎯 **Auto-detect Aplikasi** - Otomatis menyesuaikan dengan aplikasi presentasi
- 📱 **Universal Compatibility** - Bekerja dengan PowerPoint, Google Slides, Canva, PDF
- 🌐 **Online & Offline** - Dukungan voice recognition online (Google) dan offline (Vosk)
- 🎨 **Visual Feedback** - UI overlay menampilkan status real-time
- 🔊 **Sound Effects** - Audio feedback untuk setiap command (opsional)

## 🎮 Gesture yang Didukung

| Gesture | Command | Aksi |
|---------|---------|------|
| 👉 Swipe Kanan | Next | Slide berikutnya |
| 👈 Swipe Kiri | Previous | Slide sebelumnya |
| ✋ Open Palm | Pause | Pause/Blackout |
| ✊ Closed Fist | Play | Resume |
| 👍 Thumbs Up | First | Slide pertama |
| 👎 Thumbs Down | Last | Slide terakhir |
| ✌️ Peace Sign | Blackout | Layar hitam |

## 🗣️ Perintah Suara

### Bahasa Indonesia
- **Navigasi**: "lanjut", "berikutnya", "kembali", "sebelumnya", "pertama", "terakhir"
- **Kontrol**: "berhenti", "jeda", "lanjutkan", "mulai", "keluar"

### English
- **Navigation**: "next", "previous", "back", "first", "last", "start", "end"
- **Control**: "pause", "stop", "play", "resume", "exit", "quit"

## 📋 Requirements

- Python 3.8 atau lebih tinggi
- Webcam
- Microphone (untuk voice control)
- Windows 10/11 (Linux/Mac juga didukung dengan modifikasi)

## 🚀 Instalasi

### 1. Clone Repository

```powershell
git clone https://github.com/rab781/Presentation-Tools.git
cd Presentation-Tools
```

### 2. Buat Virtual Environment (Opsional tapi Direkomendasikan)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

#### Instalasi Standar
```powershell
pip install -r requirements.txt
```

#### ⚠️ Instalasi PyAudio di Windows

PyAudio sering bermasalah saat instalasi di Windows. Gunakan salah satu metode berikut:

**Metode 1: Menggunakan pipwin**
```powershell
pip install pipwin
pipwin install pyaudio
```

**Metode 2: Download Pre-built Wheel**
1. Download dari [Unofficial Windows Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
2. Pilih sesuai Python version dan architecture (contoh: `PyAudio-0.2.13-cp311-cp311-win_amd64.whl` untuk Python 3.11 64-bit)
3. Install:
```powershell
pip install PyAudio-0.2.13-cp311-cp311-win_amd64.whl
```

**Metode 3: Install Microsoft C++ Build Tools**
1. Download [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Install dengan komponen "Desktop development with C++"
3. Restart dan coba install ulang PyAudio

### 4. Download Vosk Model untuk Offline Voice Recognition (Opsional)

Untuk mode offline, download model bahasa Indonesia:

```powershell
# Buat folder models
mkdir models
cd models

# Download model (pilih salah satu)
# Small model (~50MB) - Recommended
Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-small-id-0.22.zip" -OutFile "vosk-model-small-id-0.22.zip"

# Extract
Expand-Archive -Path "vosk-model-small-id-0.22.zip" -DestinationPath "."

cd ..
```

Model lain tersedia di: https://alphacephei.com/vosk/models

## 🎯 Cara Penggunaan

### Quick Start

```powershell
python main.py
```

### Mode Operasi

Saat aplikasi berjalan, tekan tombol berikut untuk switch mode:

- **G** - Gesture Only (hanya gerakan tangan)
- **V** - Voice Only (hanya suara)
- **H** - Hybrid (gesture + voice)

### Tombol Kontrol

| Key | Fungsi |
|-----|--------|
| **G** | Switch to Gesture Only mode |
| **V** | Switch to Voice Only mode |
| **H** | Switch to Hybrid mode |
| **C** | Run calibration wizard |
| **A** | Auto-detect active application |
| **P** | Pause/Resume detection |
| **ESC** | Exit application |

### Calibration

Sebelum presentasi pertama kali, jalankan calibration:

```powershell
python main.py --calibrate
```

Calibration wizard akan:
- Test camera
- Test microphone
- Test keyboard control
- Detect aplikasi presentasi
- Memberikan rekomendasi setup

## 🖥️ Supported Applications

| Application | Auto-detect | Shortcuts | Status |
|-------------|-------------|-----------|--------|
| PowerPoint | ✅ | ✅ | Fully supported |
| Google Slides | ✅ | ✅ | Fully supported |
| PDF Viewers | ✅ | ✅ | Supported |
| Canva | ✅ | ⚠️ | Limited support |
| Universal | - | ✅ | Fallback mode |

### Application-Specific Shortcuts

Tool ini otomatis mendeteksi aplikasi yang sedang aktif dan menggunakan keyboard shortcuts yang sesuai:

- **PowerPoint**: F5 (start), Arrow keys, B (blackout)
- **Google Slides**: Ctrl+F5 (start), Arrow keys, S (speaker notes)
- **PDF Viewers**: Arrow keys, Page Up/Down
- **Universal**: Arrow keys, Home, End, ESC

## ⚙️ Konfigurasi

Edit file `config.py` atau buat `user_config.json` untuk customize:

```json
{
  "mode": "hybrid",
  "gesture_sensitivity": 0.7,
  "voice_sensitivity": 0.6,
  "debounce_time": 0.5,
  "camera_index": 0,
  "show_ui": true,
  "sound_effects": true,
  "offline_mode": false,
  "language": "both"
}
```

### Parameter Konfigurasi

- **mode**: `"gesture"`, `"voice"`, atau `"hybrid"`
- **gesture_sensitivity**: 0.0 - 1.0 (tinggi = lebih sensitif)
- **voice_sensitivity**: 0.0 - 1.0
- **debounce_time**: Waktu delay antar command (detik)
- **camera_index**: Index camera (0 = default, 1 = external)
- **show_ui**: Tampilkan UI overlay
- **sound_effects**: Aktifkan sound feedback
- **offline_mode**: Gunakan Vosk untuk offline recognition
- **language**: `"indonesian"`, `"english"`, atau `"both"`

## 🔧 Troubleshooting

### Camera tidak terdeteksi
```powershell
# Test camera dengan OpenCV
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error')"
```

### Microphone tidak bekerja
- Pastikan microphone permission diaktifkan di Windows Settings
- Test dengan: `python main.py --calibrate`
- Coba adjust energy threshold di `config.py`

### Gesture tidak terdeteksi
- Pastikan pencahayaan cukup terang
- Jarak tangan ke camera: 0.5 - 2 meter
- Tangan harus terlihat penuh oleh camera
- Gunakan background yang kontras

### Voice recognition tidak akurat
- Kurangi background noise
- Bicara dengan jelas dan tidak terlalu cepat
- Untuk offline mode, pastikan Vosk model sudah terinstall
- Adjust `energy_threshold` di `config.py`

### Keyboard shortcuts tidak bekerja
- Pastikan aplikasi presentasi dalam focus (klik window presentasi)
- Coba manual detect dengan tekan **A**
- Beberapa aplikasi mungkin perlu admin privileges
- Test dengan: `controller.test_command("next")`

### PyAutoGUI failsafe triggered
- Jangan gerakkan mouse ke pojok kiri atas terlalu cepat
- Failsafe sudah disabled di code, tapi bisa re-enable jika perlu

### High CPU usage
- Kurangi FPS camera di `gesture_detector.py`
- Disable UI overlay dengan set `show_ui: false`
- Gunakan mode voice-only jika gesture tidak diperlukan

## 📁 Struktur Project

```
Presentation-Tools/
│
├── main.py                    # Main application
├── gesture_detector.py        # Hand gesture detection
├── voice_recognizer.py        # Voice command recognition
├── controller.py              # Keyboard controller & calibration
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation (this file)
│
├── models/                    # Vosk models (offline)
│   └── vosk-model-small-id-0.22/
│
└── user_config.json           # User preferences (auto-generated)
```

## 🎓 Tips untuk Presentasi

1. **Sebelum Presentasi**
   - Jalankan calibration wizard
   - Test semua gestures
   - Test voice commands
   - Posisikan camera dengan baik
   - Check pencahayaan ruangan

2. **Saat Presentasi**
   - Start aplikasi sebelum buka presentasi
   - Gunakan mode Hybrid untuk flexibility
   - Tangan santai, tidak perlu tegang
   - Bicara dengan jelas untuk voice commands
   - Gunakan **P** untuk pause jika tidak ingin ada deteksi sementara

3. **Best Practices**
   - Jangan berdiri terlalu dekat/jauh dari camera
   - Hindari gerakan tangan yang tidak perlu
   - Gunakan gesture yang paling nyaman untuk Anda
   - Practice beberapa kali sebelum presentasi sebenarnya

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **MediaPipe** by Google for hand tracking
- **OpenCV** for computer vision
- **SpeechRecognition** for voice recognition
- **Vosk** for offline speech recognition
- **PyAutoGUI** for keyboard automation

## 📧 Support

Jika mengalami masalah atau ada pertanyaan:
1. Check [Troubleshooting](#-troubleshooting) section
2. Run calibration wizard: `python main.py --calibrate`
3. Open an issue di GitHub
4. Contact: [Your Email/Contact]

## 🚀 Future Features

- [ ] Hand gesture customization
- [ ] Multiple language support
- [ ] Remote control via smartphone
- [ ] Cloud sync untuk settings
- [ ] Gesture recording dan replay
- [ ] Integration dengan PowerPoint API
- [ ] Machine learning untuk custom gestures
- [ ] Web-based control panel

---

**Made with ❤️ for better presentations**

*Happy Presenting! 🎤✨*
