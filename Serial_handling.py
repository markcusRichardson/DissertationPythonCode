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

def connect_arduino(port):
    try:
        return serial.Serial(port, BAUD_RATE, timeout=1)
    except Exception as e:
        # print(f"⚠️ Warning: Could not connect to {port}: {e}")
        return None

arduino_1 = connect_arduino(SERIAL_PORT_1)
arduino_2 = connect_arduino(SERIAL_PORT_2)

# Decode data from Arduino 1
def arduino1_decode(PORT_SERIAL):
    if PORT_SERIAL and PORT_SERIAL.in_waiting >= 20:
        START = PORT_SERIAL.read(1)
        if START == bytes([START_BYTE]):
            DATA1 = PORT_SERIAL.read(20)
            END = PORT_SERIAL.read(1)
            if END == bytes([END_BYTE]):
                try:
                    longitude, latitude, altitude, speed, satellites, date, time, timem, alarm_bool = struct.unpack("fffBHHHHB", DATA1)
                    configV.longitude = longitude
                    configV.latitude = latitude
                    configV.altitude = altitude
                    configV.speed = speed
                    configV.satellites = satellites
                    configV.date = date
                    configV.time = time
                    configV.timem = timem
                    configV.alarm_bool = bool(alarm_bool)
                except struct.error as e:
                    print(f"Decoding Error: {e}")

# Decode data from Arduino 2
def arduino2_decode(PORT_SERIAL1):
    if PORT_SERIAL1 and PORT_SERIAL1.in_waiting >= 5:
        START = PORT_SERIAL1.read(1)
        if START == bytes([START_BYTE]):
            radar_reading = int.from_bytes(PORT_SERIAL1.read(1), "little")
            segments = int(PORT_SERIAL1.read(2))
            END = PORT_SERIAL1.read(1)
            if END == bytes([END_BYTE]):
                configV.radar_reading = radar_reading
                configV.segments = segments

# Encode and send data to Arduino
def arduino_encode(serial_port, mode, brightnessFront, brightnessRear, brightnessMiddle, lock_state, alarm_state, brightnessLogo, alarm_bool_reset):
    if serial_port:
        try:
            lock_state = int(lock_state)  # Convert bool to byte (0 or 1)
            alarm_state = int(alarm_state)
            alarm_bool_reset = int(alarm_bool_reset)
            packet = struct.pack("BBBBBBBB", mode, lock_state, alarm_state, brightnessFront, brightnessMiddle, brightnessRear, brightnessLogo, alarm_bool_reset)
            serial_port.write(bytes([START_BYTE]))
            serial_port.write(packet)
            serial_port.write(bytes([END_BYTE]))
        except Exception as e:
            print(f"Serial Encoding Error: {e}")

def serial_task():
    global arduino_1, arduino_2
    while True:
        try:
            if arduino_1 is None:
                arduino_1 = connect_arduino(SERIAL_PORT_1)
            if arduino_2 is None:
                arduino_2 = connect_arduino(SERIAL_PORT_2)

            if arduino_1:
                arduino1_decode(arduino_1)
                arduino_encode(arduino_1, configV.mode, configV.brightnessFront, configV.brightnessRear, configV.brightnessMiddle, configV.lock_state, configV.alarm_bool, configV.brightnessLogo, configV.alarm_bool_reset)

            if arduino_2:
                arduino2_decode(arduino_2)

        except serial.SerialException as e:
            print(f"[ERROR] Serial Connection Lost: {e}")
            time.sleep(2)  # Wait before retrying

        time.sleep(0.1)

