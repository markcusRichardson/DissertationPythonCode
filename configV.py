# =======================================================
# Smart Bike System – Global Configuration Variables
# -------------------------------------------------------
# This file contains all globally shared variables used
# across the different modules:
#   - Serial data handlers (for Arduino)
#   - MQTT handlers (for mobile/cloud communication)
#   - GUI dashboard (Tkinter)
#   - Thread management
#
# Acts as a central repository for current sensor readings,
# system state, and configuration settings.
# =======================================================

# -------------------------------------------------------
# Control State & LED Brightness Settings
# -------------------------------------------------------
mode = 0                   # Current operating mode (0–4, set by user or app)
lock_state = False         # Bike locked (True) or unlocked (False)
brightnessFront = 0        # Front LED strip brightness (0–100)
brightnessRear = 0         # Rear LED strip brightness
brightnessMiddle = 0       # Middle frame lighting
brightnessLogo = 0         # Logo or branding light brightness

# -------------------------------------------------------
# GPS / Navigation Data
# -------------------------------------------------------
longitude = 0.0            # Current GPS longitude
latitude = 0.0             # Current GPS latitude
altitude = 0.0             # Altitude in meters
satellites = 0             # Number of satellites connected
date = 0                   # Date in compact format (e.g., DDMM)
speed = 0.0                # Speed in km/h
time = 0                   # Time (hour/min) from GPS
timem = 0                  # Minute portion (optional split)
alarm_bool = False         # Alarm trigger flag
alarm_bool_reset = False   # Reset signal from app/user to clear alarm

# -------------------------------------------------------
# Radar / Proximity Sensor Data
# -------------------------------------------------------
radar_reading = 0          # Raw radar event ID (0–4)
radar_output = ""          # Human-readable description (e.g., "Approaching Detected")
segments = 0               # Encoded bitmask for obstacle segments/zones
