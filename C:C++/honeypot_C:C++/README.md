# Modular Honeypot (C++ Version)

**Modular Honeypot** is a lightweight, modular honeypot system written in **C++**. It allows users to listen on specified ports, log incoming connections and data, and generate a summary report after the session ends.

> This is the C++ version of the honeypot system. A Python version is also available in this repository.

---

## Features

- Multi-threaded port listeners using `std::thread`
- Live logging of incoming connections and received messages
- Session-based folder creation with timestamped logs
- Text-based session summary generation
- Graceful shutdown using `SIGTERM` handling
- Simple CLI interface for selecting ports
- Platform: **Linux / Unix-like systems**

---

## Structure

```
project/
├── CMakeLists.txt
├── main.cpp
├── honeypot.hpp
├── honeypot.cpp
├── .gitignore
└── honeypot_logs/
    └── session_YYYY-MM-DD_HH-MM-SS/
        ├── port_<PORT>.log
        └── summary.txt
```

---

## Usage

### Run via Terminal or CLion

1. Compile using `CMake` or CLion (auto-handled)
2. Run the binary:
```bash
./ModularHoneypot
```

3. Example input:
```
=== Modular Honeypot (C++) ===
Enter ports to listen on (comma-separated), or press Enter for default: 21,22,80
```

4. Connect using `nc` or similar:
```bash
nc localhost 80
```

5. Type any message, and it will be logged.

6. To stop the program gracefully:
```bash
Ctrl + C
```

---

## Output

Logs are saved in:
```
honeypot_logs/session_YYYY-MM-DD_HH-MM-SS/
```

Each port gets its own `.log` file. At the end of the session, a `summary.txt` is created with session metadata.

---

## Requirements

- C++17 or newer
- Linux (for POSIX sockets and signal handling)
- CMake (to build)

---

## Future Enhancements

- Support for UDP
- Visual log viewer
- Integration with external analytics (ELK stack, etc.)
- Configurable triggers or alerting

---

## Example Log Entry

**port_80.log**
```
[RECEIVED] Connection from 203.0.113.42 on port 80
```

---

## Related Projects

- [Python Honeypot Version](https://github.com/ziulko/PORTFOLIO/tree/main/Python/honeypot_python)
