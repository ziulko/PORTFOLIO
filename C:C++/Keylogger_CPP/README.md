# Educational Keylogger (C++ | macOS & Linux)

**Educational Keylogger** is a lightweight, cross-platform demonstration tool written in **C++** for studying how keylogging and active window tracking work at the system level. It captures keystrokes and associates them with the active application, logging everything to session-based files.

> This project is strictly for **educational and ethical cybersecurity research**. Do **not** use this tool on any system without full consent.

---

## Features

- Real-time keystroke logging
- Active window / application tracking
- Daily folder creation with session-based logs
- Supports both **macOS** (Quartz Event Taps) and **Linux** (X11 planned)
- Graceful shutdown with `SIGTERM` / `SIGINT` handling
- Cross-platform structure using `CMake`
- No third-party dependencies (on macOS)

---

## Structure

```
Keylogger/
├── CMakeLists.txt
├── main.cpp
├── keylogger_interface.h
├── keylogger_macos.cpp
├── active_window_utils.h
├── active_window_macos.cpp
├── logger_utils.h
├── logger_utils.cpp
├── .gitignore
└── logs/
    └── YYYY-MM-DD/
        ├── session_1.txt
        ├── session_2.txt
        └── ...
```

---

## Usage

### macOS

1. Grant **Input Monitoring** and **Accessibility** permissions in `System Settings > Privacy & Security`.
2. Build the project via `CMake` or CLion.
3. Run the compiled binary:
```bash
./Keylogger
```

4. Type in any application. The keystrokes will be logged.
5. Logs are saved in:
```
logs/YYYY-MM-DD/session_N.txt
```
6. To terminate the program gracefully:
```bash
Ctrl + C
# or
kill <pid>
```

---

## Output

Each session creates a timestamped file in the daily `logs/` folder:

**Example log:**
```
--- Switched to: Terminal ---
hello world

--- Switched to: Safari ---
searching C++ keylogger examples...
```

---

## Requirements

- macOS (tested on Monterey and newer)
- C++17 or newer
- CMake 3.10+
- Full access permissions for Input Monitoring

> Linux support (X11) coming soon.

---

## Future Enhancements

- Wayland-compatible Linux version
- Unicode/Emoji character support
- Optional CLI flags (e.g., log path, verbosity)
- Encrypted log storage
- GUI for real-time visualization

---

## Warning

This tool is **not intended for malicious use**. Use it **only in controlled environments** with full user awareness and consent. Unauthorized use may violate laws and ethical standards.

