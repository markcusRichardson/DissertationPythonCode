import threading
import time
import Serial_handling
import mqtt_handler
import screen_system

def start_threads():
    print("[MAIN] Starting serial and MQTT threads...")
    gui_thread=threading.Thread(target=screen_system.start_screen, daemon=True)
    serial_thread = threading.Thread(target=Serial_handling.serial_task, daemon=True)
    mqtt_thread = threading.Thread(target=mqtt_handler.mqtt_task, daemon=True)
    gui_thread.start()
    time.sleep(1)
    serial_thread.start()
    mqtt_thread.start()

start_threads()  # Start serial and MQTT tasks
