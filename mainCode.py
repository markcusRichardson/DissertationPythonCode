import threading
import time
import Serial_handling
import mqtt_handler

def start_threads():
    print("[MAIN] Starting serial and MQTT threads...")
    
    # Start the serial handling thread
    serial_thread = threading.Thread(target=Serial_handling.serial_task, daemon=True)
    serial_thread.start()
    
    # Start the MQTT handling thread
    mqtt_thread = threading.Thread(target=mqtt_handler.mqtt_task, daemon=True)
    mqtt_thread.start()

if __name__ == "__main__":
    start_threads()  # Start serial and MQTT tasks
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)  # Sleep to prevent busy waiting
    except KeyboardInterrupt:
        print("[MAIN] Exiting...")