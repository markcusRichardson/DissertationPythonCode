import serial
import struct
import configV

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
def arduino1_decode(SERIAL):
    if SERIAL and SERIAL.in_waiting >= 20:
        START = SERIAL.read(1)

        if START == bytes([START_BYTE]):
            DATA1 = SERIAL.read(18)
            END = SERIAL.read(1)

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
def arduino2_decode(SERIAL):
    if SERIAL and SERIAL.in_waiting >= 5:
        START = SERIAL.read(1)

        if START == bytes([START_BYTE]):
            radar_reading = int.from_bytes(SERIAL.read(1), "little")
            segments = list(SERIAL.read(2))
            END = SERIAL.read(1)

            if END == bytes([END_BYTE]):
                configV.radar_reading = radar_reading
                configV.segments = segments

# Encode and send data to Arduino
def arduino_encode(serial_port, mode, brightnessFront, brightnessRear, brightnessMiddle, lock_state, alarm_state, brightnessLogo):
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
    arduino1_decode(arduino_1)
    arduino2_decode(arduino_2)

    arduino_encode(arduino_1, configV.mode, configV.brightnessFront, configV.brightnessRear, configV.brightnessMiddle, configV.lock_state, configV.alarm_bool, configV.brightnessLogo)
