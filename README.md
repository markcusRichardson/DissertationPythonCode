# Smart Bike System – Raspberry Pi & Arduino Integration

This repository forms the software foundation for a **Smart Bike System** designed as part of a university-level engineering dissertation. The system integrates multiple sensors and control interfaces across a network of two Arduino microcontrollers and a Raspberry Pi, with live feedback to a mobile application via MQTT.

---

## 🧠 System Overview

The system provides **real-time data acquisition, processing, display, and remote control** for an e-bike, incorporating:

- GPS and IMU data for location, speed, and orientation.
- Radar-based proximity detection.
- Infrared motion sensing for security.
- Addressable LEDs for visibility and signaling.
- A handlebar-mounted 3.5" touchscreen for local display and control.
- MQTT communication with a smartphone interface.

---

## 📁 File Structure and Purpose

| File/Module               | Description |
|--------------------------|-------------|
| `main.py`                | Entry point for the system. Launches concurrent threads for serial and MQTT communication. Keeps the system running indefinitely. |
| `Serial_handling.py`     | Manages all serial communication with the two Arduinos. Parses sensor data from Arduino 1 (GPS, IMU, Alarm) and radar data from Arduino 2. Sends control packets back (LED brightness, lock state, etc.). |
| `mqtt_handler.py`        | Handles bidirectional MQTT communication. Receives user commands (e.g., lock, mode change) and publishes telemetry data (speed, location, radar status). |
| `gui_display.py`         | (Optional) Tkinter-based GUI module for the Raspberry Pi’s 3.5" screen. Displays speed, GPS, brightness, and provides a rotary-encoder navigable menu. |
| `configV.py`             | Shared configuration file that holds global variables accessed across all modules. Acts as a real-time memory store for system state. |
| `README.md`              | This documentation file describing the purpose and structure of the system. |

---

## ⚙️ Hardware Components

- **Raspberry Pi 4** (main controller & display unit)
- **Arduino Uno / Nano (x2)**:
  - *Arduino 1*: GPS, IMU, Alarm
  - *Arduino 2*: Radar sensor (HC-SR04 or similar)
- **Rotary Encoder with Push Button**
- **3.5" Pi Touchscreen (800x480)**
- **Addressable RGB LED strips (WS2812)**
- **Piezo buzzer or speaker for alarm feedback**
- **Battery pack with 5V rail**
- **Mobile phone running MQTT client app (e.g., IoT MQTT Panel)**

---

## 🔄 Threaded Architecture

The Pi executes the system via **multi-threaded Python**, with:

- `Serial_handling.serial_task()`: continuously reads from and writes to the Arduinos.
- `mqtt_handler.mqtt_task()`: manages MQTT session, subscriptions, and telemetry publication.
- `gui_display.start_screen()`: (if used) runs the display UI in the main thread.

All threads share data via the `configV.py` global variables module.

---

## 📡 MQTT Topics

The MQTT communication protocol uses the following topics (with topic names under `bike/`):

### 📥 Subscribed Topics (from App → Pi)
- `bike/lock` — Lock/unlock bike
- `bike/mode` — Set ride mode (e.g., eco, sport)
- `bike/brightness/front` — LED brightness settings
- `bike/brightness/rear`
- `bike/brightness/middle`
- `bike/brightness/logo`
- `bike/alarmReset` — Clear/reset alarm status

### 📤 Published Topics (from Pi → App)
- `bike/speed`, `bike/latitude`, `bike/longitude`, `bike/altitude`, `bike/satellites`
- `bike/radar` — Segment status (proximity zones)
- `bike/radar_reading` — Human-readable detection state
- `bike/alarm` — Notifies app if alarm is triggered

---

## ✅ System Workflow Summary

1. Arduinos gather data and transmit it via serial.
2. Pi receives and parses data using `Serial_handling.py`.
3. `configV.py` holds shared state for all modules.
4. `mqtt_handler.py` sends data to the app and listens for commands.
5. Optionally, `gui_display.py` shows real-time feedback on a local screen.

---

## 📘 Integration in Dissertation Report

This repository and its file descriptions are referenced in the **Software Implementation** chapter of the dissertation. Each script corresponds to a modular section described in:
- System Architecture Diagram
- Threaded Operation Explanation
- Communication Stack (Serial + MQTT)
- User Interface Design

---

## 🔒 Notes on Security & Safety

- Alarm logic can be triggered from motion detection or unauthorized access.
- MQTT communication assumes secure local broker — in future work, TLS could be added.
- System stability ensured by modular thread isolation and watchdog recovery behavior.

---

## 🛠 Future Enhancements (Beyond Dissertation)

- OTA firmware updates via MQTT
- Cloud data logging via AWS IoT or Google Cloud MQTT
- Expanded menu UI with touch support
- Enhanced collision avoidance via ML-driven radar pattern classification

---

For detailed explanations, circuit diagrams, and test results, please refer to the full dissertation document.
