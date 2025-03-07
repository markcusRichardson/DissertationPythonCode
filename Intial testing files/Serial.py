import serial
import time
time.sleep(10)

arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

time.sleep(2)

while True:
	if arduino.in_waiting:
		DATA = 	arduino.readline().decode("utf-8").strip()
		print(f"Received: {DATA}")
