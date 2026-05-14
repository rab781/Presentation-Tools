# Reference: Keyboard Controls

This reference details the keyboard shortcuts available when the Presentation Control Tool is running and the webcam window is active.

## Application Controls

While the application is active, you press these keys on your keyboard to control its behavior:

| Key | Function | Description |
|-----|----------|-------------|
| **G** | Gesture Mode | Switches the application to Gesture Only mode. |
| **V** | Voice Mode | Switches the application to Voice Only mode. |
| **H** | Hybrid Mode | Switches the application to Hybrid mode (default), listening for both gestures and voice. |
| **C** | Calibrate | Runs the calibration wizard to test your setup. |
| **A** | Auto-detect | Manually triggers detection of the active presentation application. |
| **P** | Pause | Pauses or resumes detection of gestures and voice. |
| **ESC** | Exit | Exits the application entirely. |

## Presentation Software Mappings

When the tool detects a specific presentation software, it maps the logical commands (like "next" or "previous") to specific keyboard outputs sent to that application.

The current mappings are defined internally in the `APP_PROFILES` configuration:

### PowerPoint

| Logical Command | Keyboard Output |
|-----------------|-----------------|
| `next` | Right Arrow |
| `previous` | Left Arrow |
| `first` | Home |
| `last` | End |
| `pause` | B |
| `play` | B |
| `blackout` | B |
| `exit` | ESC |
| `start_presentation` | F5 |

### Google Slides

| Logical Command | Keyboard Output |
|-----------------|-----------------|
| `next` | Right Arrow or Space |
| `previous` | Left Arrow or Backspace |
| `first` | Home |
| `last` | End |
| `pause` | S |
| `play` | S |
| `blackout` | B |
| `exit` | ESC |
| `start_presentation` | Ctrl + F5 |

### PDF Viewer

| Logical Command | Keyboard Output |
|-----------------|-----------------|
| `next` | Right Arrow or Page Down |
| `previous` | Left Arrow or Page Up |
| `first` | Home |
| `last` | End |
| `exit` | ESC |
| `start_presentation` | F5 |
