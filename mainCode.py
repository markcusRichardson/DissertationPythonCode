import threading
import Serial_handling
import mqtt_handler
import screen_system

# Create threads for each task
serial_thread = threading.Thread(target=Serial_handling.serial_task, daemon=True)
mqtt_thread = threading.Thread(target=mqtt_handler.mqtt_task, daemon=True)




# Start all threads
serial_thread.start()
mqtt_thread.start()
screen_thread.start()

# Keep the main script running
try:
    while True:
        pass  
except KeyboardInterrupt:
    pass
