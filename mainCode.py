import threading
import time
import Serial_handling
import mqtt_handler
import screen_system

def start_threads():
    serial_thread = threading.Thread(target=Serial_handling.serial_task, daemon=True)
    mqtt_thread = threading.Thread(target=mqtt_handler.mqtt_task, daemon=True)

    serial_thread.start()
    mqtt_thread.start()

# Start the GUI
if __name__ == "__main__":
    start_threads()  # Start serial and MQTT tasks
    screen_system.dashboard_setup()  # Initialize the GUI
    screen_system.update_display()  # Start updating the GUI
    screen_system.root.mainloop()  # Run Tkinter GUI loop
