# Importing all neccasary libraries
from gpiozero import RotaryEncoder, Button
from signal import pause
import tkinter as tk
from tkinter import ttk
import serial
import time
import threading
import paho.mqtt.client as mqtt

# Define serial comms variables
SERIAL_PORT_1 = "/dev/ttyUSB0"  
SERIAL_PORT_2 = "/dev/ttyUSB1"  
BAUD_RATE = 9600

# MQTT variables
MQTT_BROKER = "IP Address"
MQTT_PORT = 1883
MQTT_TOPIC_SUBSCRIBE = "bike/control"
MQTT_TOPIC_PUBLISH = "bike/data"
client = mqtt.Client()

# Rotary encoder 
menu = ["Brightness"]
current_option = 0
rotary = RotaryEncoder(17, 18, max_steps=10)
button = Button(27)

# Screen setup
root = tk.Tk()
root.title("E-Bike dashbaoridng")
root.geometry("1920x1080")
root.configure(bg="black")
menu_label = tk.Label(root, text=menu[current_option], font=("Helvetica", 48), fg="white", bg="black")
menu_label.pack(pady=200)


# Setup Serial with arduinos
try:
    arduino_1 = serial.Serial(SERIAL_PORT_1, BAUD_RATE, timeout=1)
    arduino_2 = serial.Serial(SERIAL_PORT_2, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"Error initializing serial ports: {e}")
    arduino_1, arduino_2 = None, None



# Rotary encoder menu scolling UI
def scroll_menu ():
	global current_option
	current_option = rotary.steps % len(menu)
	print(f"selected: {menu[current_option]}")
def select_option():
	print(f"Clicked: {menu[current_option]}")
	if menu[current_option] == "exit":
		print("Exiting program...")
		exit()
rotary.when_rotated = scroll_menu
button.when_pressed = select_option




# Setup threading

thread1 = threading.Thread(target=SerialRead, daemon=True)
thread2 = threading.Thread(target=SerialWrite, daemon=True)
thread3 = threading.Thread(target=ScreenUpdates, daemon=True)
thread4 = threading.Thread(target=MQTT, daemon=True)
