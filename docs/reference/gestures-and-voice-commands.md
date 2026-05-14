# Reference: Gestures and Voice Commands

This reference details the supported hand gestures and voice commands available in the Presentation Control Tool. Use this information to understand the available inputs for controlling your presentations.

## Hand Gestures

The application recognizes the following hand gestures. Hold the gesture briefly (default 0.3 seconds) within view of the webcam to trigger the action.

| Gesture | Logical Command | Default Action |
|---------|-----------------|----------------|
| 👉 Swipe Right | `next` | Next slide |
| 👈 Swipe Left | `previous` | Previous slide |
| ✋ Open Palm | `pause` | Pause presentation / Blackout screen |
| ✊ Closed Fist | `play` | Resume presentation |
| 👍 Thumbs Up | `first` | Go to first slide |
| 👎 Thumbs Down | `last` | Go to last slide |
| ✌️ Peace Sign | `blackout` | Black screen |

## Voice Commands

The application supports both English and Indonesian voice commands. The active language is determined by the `language` configuration setting (`"english"`, `"indonesian"`, or `"both"`).

### Navigation Commands

| Logical Command | English Phrases | Indonesian Phrases |
|-----------------|-----------------|--------------------|
| `next` | "next" | "lanjut", "berikutnya", "selanjutnya" |
| `previous` | "previous", "back" | "kembali", "sebelumnya", "mundur" |
| `first` | "first", "start" | "pertama", "awal", "mulai" |
| `last` | "last", "end" | "terakhir", "akhir" |

### Control Commands

| Logical Command | English Phrases | Indonesian Phrases |
|-----------------|-----------------|--------------------|
| `pause` | "pause", "stop" | "berhenti", "jeda" |
| `play` | "play", "resume" | "lanjutkan", "mulai" |
| `blackout` | "black", "blackout" | "hitam", "gelap" |
| `exit` | "exit", "quit", "close"| "keluar", "tutup" |
