# Cara Menggunakan Presentation Control Tool

## 🚀 Quick Start

### 1. Aktifkan Virtual Environment & Jalankan
```powershell
# Jalankan aplikasi
.\venv\Scripts\python.exe main.py
```

### 2. Pilih Mode Operasi
Setelah aplikasi berjalan, tekan:
- **G** = Gesture Only (hanya gerakan tangan)
- **V** = Voice Only (hanya suara)
- **H** = Hybrid (gesture + voice)

---

## 🎯 Setup untuk Presentasi

### Langkah-langkah:

1. **Buka aplikasi presentasi Anda** (PowerPoint, Google Slides, PDF, dll)

2. **Jalankan tool**
   ```powershell
   .\venv\Scripts\python.exe main.py
   ```

3. **Pilih aplikasi yang akan dikontrol:**
   
   **Opsi A: Auto-Detect (Otomatis)**
   - Tekan **A** untuk auto-detect
   - Tool akan mendeteksi aplikasi aktif secara otomatis
   
   **Opsi B: Manual Selection (Pilih Manual)**
   - Tekan **S** untuk membuka menu seleksi
   - Atau langsung tekan angka:
     - **1** = PowerPoint
     - **2** = Google Slides
     - **3** = PDF Viewer
     - **4** = Canva
     - **5** = Universal (works with any app)

4. **Start presentasi** (F5 di PowerPoint)

5. **Kontrol dengan gesture atau voice!**

---

## 🎮 Kontrol Keyboard

| Key | Fungsi |
|-----|--------|
| **G** | Switch ke Gesture mode |
| **V** | Switch ke Voice mode |
| **H** | Switch ke Hybrid mode |
| **A** | Auto-detect aplikasi aktif |
| **S** | Menu pilih aplikasi manual |
| **1-5** | Pilih aplikasi langsung |
| **C** | Run calibration |
| **P** | Pause/Resume detection |
| **ESC** | Exit aplikasi |

---

## 👋 Gesture Controls

| Gesture | Command | Action |
|---------|---------|--------|
| **Swipe Right** | Next | Slide berikutnya |
| **Swipe Left** | Previous | Slide sebelumnya |

**Tips:**
- Gerakkan tangan melintasi camera dari kiri ke kanan (atau sebaliknya)
- Jarak ideal: 0.5 - 2 meter dari camera
- Pencahayaan yang baik sangat penting

---

## 🎤 Voice Commands

### Bahasa Indonesia
- "**lanjut**" / "**berikutnya**" → Next slide
- "**kembali**" / "**sebelumnya**" → Previous slide
- "**pertama**" / "**awal**" → First slide
- "**terakhir**" / "**akhir**" → Last slide

### English
- "**next**" → Next slide
- "**previous**" / "**back**" → Previous slide
- "**first**" / "**start**" → First slide
- "**last**" / "**end**" → Last slide

**Tips:**
- Bicara dengan jelas dan tidak terlalu cepat
- Kurangi background noise
- Jarak ideal dari microphone: 0.5 - 1 meter

---

## 🔧 Troubleshooting

### Aplikasi tidak terdeteksi dengan benar?

**Solusi 1: Auto-detect ulang**
```
1. Klik pada window presentasi (pastikan aktif)
2. Tekan A di aplikasi tool
```

**Solusi 2: Pilih manual**
```
1. Tekan S untuk menu
2. Pilih aplikasi yang sesuai (1-5)
```

**Solusi 3: Gunakan Universal mode**
```
Tekan angka 5 untuk Universal mode
Mode ini menggunakan arrow keys yang bekerja di hampir semua aplikasi
```

### Commands tidak bekerja?

**Checklist:**
- ✅ Aplikasi presentasi dalam focus (klik window presentasi)
- ✅ Presentasi sudah dimulai (F5 di PowerPoint)
- ✅ Application profile sudah dipilih
- ✅ Mode detection tidak di-pause (tekan P untuk unpause)

### Gesture terlalu sensitif?

**Solusi:**
- Tekan **P** untuk pause sementara
- Switch ke **V** (voice only) saat tidak perlu gesture
- Kurangi gerakan tangan yang tidak perlu

---

## 📋 Workflow Rekomendasi

### Untuk Presentasi Formal
```
1. Jalankan tool
2. Tekan V (voice only)
3. Start presentasi
4. Gunakan voice commands
```
**Kenapa?** Lebih profesional, tidak ada gestur yang mengganggu

### Untuk Demo/Workshop
```
1. Jalankan tool
2. Tekan G (gesture only)
3. Start presentasi
4. Gunakan hand gestures
```
**Kenapa?** Lebih interaktif dan engaging

### Untuk Presentasi Penting
```
1. Jalankan tool
2. Tekan H (hybrid)
3. Start presentasi
4. Gunakan gesture atau voice sesuai kebutuhan
```
**Kenapa?** Maksimal flexibility, redundancy jika satu mode gagal

---

## 💡 Pro Tips

1. **Selalu test sebelum presentasi:**
   ```powershell
   .\venv\Scripts\python.exe main.py --calibrate
   ```

2. **Pilih aplikasi sebelum start presentasi:**
   - Tekan **S** → pilih aplikasi
   - Atau tekan **A** untuk auto-detect

3. **Pastikan window presentasi aktif:**
   - Klik window presentasi sebelum menggunakan commands

4. **Siapkan backup:**
   - Tetap sediakan keyboard atau clicker sebagai backup

5. **Practice dulu:**
   - Test semua gestures dan voice commands sebelum presentasi sebenarnya

---

## ✅ Checklist Sebelum Presentasi

- [ ] Virtual environment sudah aktif
- [ ] Calibration berhasil (`.\venv\Scripts\python.exe main.py --calibrate`)
- [ ] Camera dan microphone berfungsi
- [ ] Gesture detection tested
- [ ] Voice commands tested
- [ ] Application profile dipilih
- [ ] Presentasi sudah dibuka
- [ ] Backup control (keyboard/clicker) ready

---

## 🎯 Example Session

```powershell
# 1. Buka PowerPoint dan buka file presentasi
# 2. Jalankan tool
.\venv\Scripts\python.exe main.py

# Output:
# ============================================================
# PRESENTATION CONTROL TOOL
# ============================================================
# Mode: HYBRID
# 
# ✓ Gesture detection initialized
# ✓ Voice recognition initialized
# ✓ Controller initialized
# 
# ------------------------------------------------------------
# CONTROLS:
#   ...
# ------------------------------------------------------------

# 3. Tekan A untuk auto-detect
# Output:
# Auto-detecting application...
# Active window: 'Presentation1.pptx - PowerPoint'
# Process: 'powerpnt.exe'
# Detected application profile: powerpoint

# 4. Start presentasi (F5)

# 5. Swipe right atau katakan "next" untuk next slide!
```

---

## 📞 Bantuan Lebih Lanjut

Jika masih ada masalah:
1. Check **TROUBLESHOOTING.md** untuk solusi lengkap
2. Run diagnostic: `.\venv\Scripts\python.exe test_setup.py`
3. Run calibration: `.\venv\Scripts\python.exe main.py --calibrate`

**Happy Presenting! 🎤✨**
