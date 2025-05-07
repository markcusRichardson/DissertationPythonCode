# ==========================================
# Smart Bike System: Arduino Serial Interface
# ------------------------------------------
# This Python script handles serial communication between a Raspberry Pi and two Arduino boards 
# as part of a smart bike system. It manages:
#   - Receiving GPS, accelerometer, and alarm data from Arduino 1
#   - Receiving radar and segment data from Arduino 2
#   - Sending control data back to Arduino 1 (e.g., LED brightness, lock and alarm states)
# This file is designed to run continuously on the Raspberry Pi, parsing and updating system-wide 
# configuration variables stored in the 'configV' module.
# ==========================================

import serial         # Serial communication library
import struct         # For encoding/decoding binary data packets
import configV        # Custom configuration file to hold global variables
import time           # For delay and timing
import sys            # For system-level operations (not used directly here)

# ------------------------------------------
# Serial Port Configuration Constants
# ------------------------------------------
SERIAL_PORT_1 = "/dev/ttyUSB0"  # Arduino 1 (GPS/IMU)
SERIAL_PORT_2 = "/dev/ttyUSB1"  # Arduino 2 (Radar)
BAUD_RATE = 9600
START_BYTE = 0xAA               # Start marker for a packet
END_BYTE = 0xFF                 # End marker for a packet

# ------------------------------------------
# Attempt to Connect to an Arduino Device
# ------------------------------------------
def connect_arduino(port):
    """
    Establish a serial connection to the Arduino on the given port.
    Returns the Serial object or None if connection fails.
    """
    try:
        return serial.Serial(port, BAUD_RATE, timeout=1)
    except Exception as e:
        return None

# Initialize serial connections (if available)
arduino_1 = connect_arduino(SERIAL_PORT_1)
arduino_2 = connect_arduino(SERIAL_PORT_2)

# ------------------------------------------
# Decode GPS/IMU/Alarm Packet from Arduino 1
# ------------------------------------------
def arduino1_decode(PORT_SERIAL):
    """
    Reads and decodes a structured binary packet from Arduino 1, containing:
        - GPS coordinates (longitude, latitude, altitude)
        - Speed and satellite count
        - Date, time, alarm flag
    Updates shared config variables for use by other system modules.
    """
    while PORT_SERIAL.in_waiting > 0:
        start = PORT_SERIAL.read(1)
        if start != bytes([START_BYTE]):
            continue  # Skip any junk bytes until the packet start

        if PORT_SERIAL.in_waiting < 27:
            return  # Incomplete packet, wait for more data

        data = PORT_SERIAL.read(26)
        end = PORT_SERIAL.read(1)

        if end != bytes([END_BYTE]):
            print("[ERROR] End byte mismatch! Skipping this packet.")
            continue

        try:
            # Unpack 9 fields using little-endian format
            longitude, latitude, altitude, speed, satellites, date, time, timem, alarm_bool = struct.unpack("<ffffHHHHB", data)

            # Store decoded values into global config
            configV.longitude = longitude
            configV.latitude = latitude
            configV.altitude = altitude
            configV.speed = speed
            configV.satellites = satellites
            configV.date = date
            configV.time = time
            configV.timem = timem
            configV.alarm_bool = bool(alarm_bool)

            # Print debug info
            print(f"[DECODED] Lat: {latitude:.6f}, Long: {longitude:.6f}, Alt: {altitude:.2f} m, Speed: {speed:.2f} km/h")
            print(f"[DECODED] Sats: {satellites}, Date: {date}, Time: {time}:{timem}, Alarm: {configV.alarm_bool}")

        except struct.error as e:
            print(f"[ERROR] Struct unpacking failed: {e}")

# ------------------------------------------
# Decode Radar Packet from Arduino 2
# ------------------------------------------
def arduino2_decode(PORT_SERIAL1):
    """
    Reads radar data and segment information from Arduino 2.
    Updates config with radar distance and which segment is triggered (e.g., obstacle detection zones).
    """
    if PORT_SERIAL1 and PORT_SERIAL1.in_waiting >= 5:
        START = PORT_SERIAL1.read(1)
        if START == bytes([START_BYTE]):
            radar_reading = int.from_bytes(PORT_SERIAL1.read(1), "little")
            segments = int.from_bytes(PORT_SERIAL1.read(2), "little")
            END = PORT_SERIAL1.read(1)
            if END == bytes([END_BYTE]):
                configV.radar_reading = radar_reading
                configV.segments = 0  # Default if none are triggered

                # Find the first active segment using bitmask
                for i in range(4):
                    if segments & (1 << i):
                        configV.segments = i + 1
                        break

# ------------------------------------------
# Send LED and Control Settings to Arduino 1
# ------------------------------------------
def arduino_encode(serial_port, mode, brightnessFront, brightnessRear, brightnessMiddle, lock_state, alarm_state, brightnessLogo, alarm_bool_reset):
    """
    Encodes control parameters into a structured packet and sends it to Arduino 1.
    This includes:
        - Mode selection
        - Lock/alarm states
        - LED brightness for front, rear, middle, and logo
    """
    if serial_port:
        try:
            # Ensure boolean values are sent as integers
            lock_state = int(lock_state)
            alarm_state = int(alarm_state)
            alarm_bool_reset = int(alarm_bool_reset)

            # Pack into binary format
            packet = struct.pack("BBBBBBBB", mode, lock_state, alarm_state, brightnessFront, brightnessMiddle, brightnessRear, brightnessLogo, alarm_bool_reset)

            # Transmit to Arduino
            serial_port.write(bytes([START_BYTE]))
            serial_port.write(packet)
            serial_port.write(bytes([END_BYTE]))

            # Reset alarm acknowledgment flag
            configV.alarm_bool_reset = False

        except Exception as e:
            print(f"Serial Encoding Error: {e}")

# ------------------------------------------
# Continuous Serial Communication Loop
# ------------------------------------------
def serial_task(): 
    """
    Main loop running in a thread or process that:
        - Continuously attempts connection to both Arduinos
        - Decodes GPS and radar data
        - Sends control data (LEDs, lock, alarm) to Arduino 1
        - Acts as the communication bridge for the entire smart bike system
    """
    global arduino_1, arduino_2
    while True:
        try:
            # Reconnect if disconnected
            if arduino_1 is None:
                arduino_1 = connect_arduino(SERIAL_PORT_1)
            if arduino_2 is None:
                arduino_2 = connect_arduino(SERIAL_PORT_2)

            if arduino_1:
                arduino1_decode(arduino_1)  # Step 1: Read GPS data
                time.sleep(0.05)
                arduino_1.write(b'A')       # Step 2: Acknowledge reception
                time.sleep(0.05)
                arduino_encode(             # Step 3: Send config settings
                    arduino_1,
                    configV.mode,
                    configV.brightnessFront,
                    configV.brightnessRear,
                    configV.brightnessMiddle,
                    configV.lock_state,
                    configV.alarm_bool,
                    configV.brightnessLogo,
                    configV.alarm_bool_reset
                )

            if arduino_2:
                arduino2_decode(arduino_2)

        except serial.SerialException as e:
            print(f"[ERROR] Serial Connection Lost: {e}")
            time.sleep(2)  # Retry delay
