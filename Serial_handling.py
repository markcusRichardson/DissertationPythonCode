import serial
import configV


# Define serial comms variables
SERIAL_PORT_1 = "/dev/ttyUSB0"  
SERIAL_PORT_2 = "/dev/ttyUSB1"  
BAUD_RATE = 9600
START_BYTE = 0xAA
END_BYTE = 0xFF


# Setup Serial with arduinos
try:
    arduino_1 = serial.Serial(SERIAL_PORT_1, BAUD_RATE, timeout=1)
    arduino_2 = serial.Serial(SERIAL_PORT_2, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"Error initializing serial ports: {e}")
    arduino_1, arduino_2 = None, None



# Decode incoming serial
def arduino1_decode(SERIAL){
    if SERIAL and SERIAL.in_waiting >= 20
        START = SERIAL.read(1)

        if START == bytes([START_BYTE]):
            DATA1 = SERIAL.read(18)
            END = SERIAL.read(1)

            if END == bytes([END_BYTE])
                try:
                    longitude, latitude, altitude, speed, satellites, date, time, timem, alarm_bool = struct.unpack("fffBHBHB", data)
                    configV.longtitude = longtitude
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



}

def arduino2_decode(SERIAL){
 if SERIAL and SERIAL.in_waiting >= 5
        START = SERIAL.read(1)

        if START == bytes([START_BYTE]):
            radar_reading = int.from_bytes(SERIAL.read(1), "little")  # Read Radar Data
            segments = list(SERIAL.read(2))
            if END == bytes([END_BYTE])
                configV.radar_reading = radar_reading
                configV.segments = segments


}

def arduino_encode(serial_port, mode,brightnessFront, brightnessRear lock_state, alarm_state):

    if serial_port:
        try:
            # Construct binary packet with START_BYTE and END_BYTE
            packet = struct.pack("BBB", mode, lock_state, alarm_state, brightnessFront, brightnessRear)

            serial_port.write(bytes([START_BYTE]))  # Send Start Byte
            serial_port.write(packet)  # Send structured data
            serial_port.write(bytes([END_BYTE]))  # Send End Byte

        except Exception as e:
            print(f"Serial Encoding Error: {e}")


    while True:
        # Read from both Arduinos
        data1 = arduino_decode(arduino_1)
        data2 = arduino_decode(arduino_2)

        arduino_encode(arduino_1, configV.mode, configV.lock_state, configV.alarm_state, configV.brightnessFront, configV.brightnessRear)
        