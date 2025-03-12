import threading
import Serial_handling
import mqtt_handler
import menu_system
import screen_system

# Create threads for each task
serial_thread = threading.Thread(target=serial_handler.serial_task, daemon=True)
mqtt_thread = threading.Thread(target=mqtt_handler.mqtt_task, daemon=True)
menu_thread = threading.Thread(target=menu_system.menu_task, daemon=True)
screen_thread = threading.Thread(target=screen_display.screen_task, daemon=True)

# Start all threads
serial_thread.start()
mqtt_thread.start()
menu_thread.start()
screen_thread.start()

# Keep the main script running
while True:
    pass  # Keeps the main thread alive
