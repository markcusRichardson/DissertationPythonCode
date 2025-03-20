import threading
import time
import Serial_handling
import mqtt_handler
import screen_system  # GUI Code

def start_threads():
    print("[MAIN] Starting serial and MQTT threads...")
    serial_thread = threading.Thread(target=Serial_handling.serial_task, daemon=True)
    mqtt_thread = threading.Thread(target=mqtt_handler.mqtt_task, daemon=True)
    
    serial_thread.start()
    mqtt_thread.start()

if __name__ == "__main__":
    start_threads()  # Start serial and MQTT tasks

    print("[MAIN] Starting GUI...")
    screen_system.start_screen()  # ✅ GUI must run on the main thread!
