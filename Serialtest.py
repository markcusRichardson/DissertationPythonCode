

import serial
import time

time.sleep(10)

arduino1_port = '/dev/ttyUSB0'
arduino2_port = '/dev/tty/USB1'
baud_rate = 9600

try:
	arduino1 = serial.Serial('/dev/ttyUSB0', baud_rate, timeout=1)
	arduino2 = serial.Serial('/dev/ttyUSB1', baud_rate, timeout=1)
	time.sleep(2)
	
	print("Arduinos connected")
except Exception as e:
	print(f"No connection {e}")
	exit()

try: 
	while True:
		if arduino1.in_waiting >0:
			message1 = arduino1.readline().decode('utf-8').strip()
			print(f"Arduino1:m {message1}")
		if arduino2.in_waiting >0:
                	message2 = arduino2.readline().decode('utf-8').strip()
                	print(f"Arduino2:m {message2}")
		time.sleep(0.1)
except KeybaordInterrupt:
	print("Exiting")
finally:
	arduino1.close()
	arduino2.close()
