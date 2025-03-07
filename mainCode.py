# Importing all neccasary libraries
from signal import pause
from tkinter import ttk
import time
import threading











# Setup threading

thread1 = threading.Thread(target=SerialRead, daemon=True)
thread2 = threading.Thread(target=SerialWrite, daemon=True)
thread3 = threading.Thread(target=ScreenUpdates, daemon=True)
thread4 = threading.Thread(target=MQTT, daemon=True)
