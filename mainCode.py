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

def run_gui():
    screen_system.dashboard_setup()  # Initialize the GUI
    screen_system.update_display()  # Start updating the GUI
    screen_system.root.mainloop()  # Run Tkinter GUI loop

if __name__ == "__main__":
    start_threads()  # Start serial and MQTT tasks
    gui_thread = threading.Thread(target=run_gui, daemon=True)  # Run GUI in a separate thread
    gui_thread.start()

    while True:
        time.sleep(0.1)  # Keep the script running
