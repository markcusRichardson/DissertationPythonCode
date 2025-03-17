import serial
import struct
import configV
import time
import sys

# Define serial communication
SERIAL_PORT_1 = "/dev/ttyUSB0"
SERIAL_PORT_2 = "/dev/ttyUSB1"
BAUD_RATE = 9600
START_BYTE = 0xAA
END_BYTE = 0xFF

# Setup Serial with Arduinos
try:
    arduino_1 = serial.Serial(SERIAL_PORT_1, BAUD_RATE, timeout=1)
    arduino_2 = serial.Serial(SERIAL_PORT_2, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"Error initializing serial ports: {e}")
    arduino_1, arduino_2 = None, None

# Decode data from Arduino 1
def arduino1_decode(PORT_SERIAL):
    if PORT_SERIAL and PORT_SERIAL.in_waiting >= 20:
        START = PORT_SERIAL.read(1)

        if START == bytes([START_BYTE]):
            DATA1 = PORT_SERIAL.read(18)
            END = PORT_SERIAL.read(1)

            if END == bytes([END_BYTE]):
                try:
                    longitude, latitude, altitude, speed, satellites, date, time, timem, alarm_bool = struct.unpack("fffBHBHB", DATA1)

                    configV.longitude = longitude
                    configV.latitude = latitude
                    configV.altitude = altitude
                    configV.speed = speed
                    configV.satellites = satellites
                    configV.date = date
                    configV.time = time
                    configV.timem = timem
                    configV.alarm_bool = alarm_bool

                except struct.error as e:
                    print(f"Decoding Error: {e}")

# Decode data from Arduino 2
def arduino2_decode(PORT_SERIAL1):
    if PORT_SERIAL1 and PORT_SERIAL1.in_waiting >= 5:
        START = PORT_SERIAL1.read(1)

        if START == bytes([START_BYTE]):
            radar_reading = int.from_bytes(PORT_SERIAL1.read(1), "little")
            segments = list(PORT_SERIAL1.read(2))
            END = PORT_SERIAL1.read(1)

            if END == bytes([END_BYTE]):
                configV.radar_reading = radar_reading
                configV.segments = segments

# Encode and send data to Arduino
def arduino_encode(serial_port, mode, brightnessFront, brightnessRear, brightnessMiddle, lock_state, alarm_state, brightnessLogo):
    if serial_port is None:
        return
    if serial_port:
        try:
            # Ensure we send **7 bytes** (to match Arduino `Serial.readBytes()`)
            packet = struct.pack("BBBBBBB", mode, lock_state, alarm_state, brightnessFront, brightnessMiddle, brightnessRear, brightnessLogo)  # Extra byte for safety

            serial_port.write(bytes([START_BYTE]))
            serial_port.write(packet)
            serial_port.write(bytes([END_BYTE]))

        except Exception as e:
            print(f"Serial Encoding Error: {e}")

# Continuous Reading & Writing Loop
while True:
    # Check if Arduinos are disconnected and retry connection
    if arduino_1 is None or arduino_2 is None:
        print("⚠️ Arduinos not connected. Retrying connection...")
        try:
            if arduino_1 is None:
                arduino_1 = serial.Serial(SERIAL_PORT_1, BAUD_RATE, timeout=1)
                print("✅ Arduino 1 reconnected!")

            if arduino_2 is None:
                arduino_2 = serial.Serial(SERIAL_PORT_2, BAUD_RATE, timeout=1)
                print("✅ Arduino 2 reconnected!")

        except Exception as e:
            print(f" Serial Error: {e}")
            time.sleep(5)  # Wait before retrying
            continue  # Skip loop iteration if reconnection fails

    # Process Serial Data if Arduinos are connected
    arduino1_decode(arduino_1)
    arduino2_decode(arduino_2)
    arduino_encode(arduino_1, configV.mode, configV.brightnessFront, configV.brightnessRear, configV.brightnessMiddle, configV.lock_state, configV.alarm_bool, configV.brightnessLogo)
    
    time.sleep(0.1)
