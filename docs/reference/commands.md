# Reference: Commands

This reference outlines all available input commands to control the Presentation Control application.

## Hand Gestures

The application recognizes the following gestures when standing in view of the webcam.

| Gesture | Mapped Action | Result |
|---------|---------------|--------|
| `SWIPE_RIGHT` | `next` | Advances to the next slide |
| `SWIPE_LEFT` | `previous` | Returns to the previous slide |
| `OPEN_PALM` | `pause` | Pauses or blackouts the presentation |
| `CLOSED_FIST` | `play` | Resumes or plays the presentation |
| `THUMB_UP` | `first` | Jumps to the first slide |
| `THUMB_DOWN` | `last` | Jumps to the last slide |
| `PEACE_SIGN` | `blackout` | Displays a black screen |

## Voice Commands

The application supports English and Indonesian voice commands. The following spoken phrases map to system actions.

| Action | English Phrases | Indonesian Phrases |
|--------|-----------------|--------------------|
| `next` | next | lanjut, berikutnya, selanjutnya |
| `previous` | previous, back | kembali, sebelumnya, mundur |
| `first` | first, start | pertama, awal, mulai |
| `last` | last, end | terakhir, akhir |
| `pause` | pause, stop | berhenti, jeda |
| `play` | play, resume | lanjutkan, mulai |
| `blackout` | black, blackout | hitam, gelap |
| `exit` | exit, quit, close | keluar, tutup |

## Keyboard Controls

While the application window is active, you use the following keyboard shortcuts to control the application behavior.

| Key | Action |
|-----|--------|
| `g` | Switch to Gesture Only mode |
| `v` | Switch to Voice Only mode |
| `h` | Switch to Hybrid mode (Gesture & Voice) |
| `p` | Pause/Resume detection |
| `c` | Run the calibration wizard |
| `a` | Auto-detect the active application |
| `s` | Open the manual application selection menu |
| `1` | Force set application mode to PowerPoint |
| `2` | Force set application mode to Google Slides |
| `3` | Force set application mode to PDF Viewer |
| `4` | Force set application mode to Canva |
| `5` | Force set application mode to Universal (fallback) |
| `esc` | Exit the Presentation Control application |