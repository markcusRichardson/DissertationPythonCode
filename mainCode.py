# =======================================================
# Smart Bike System – Thread Manager (Main Execution File)
# -------------------------------------------------------
# This script launches the core background threads that run the smart bike system:
#    1. Serial communication thread (with two Arduinos for GPS, radar, etc.)
#    2. MQTT communication thread (to send/receive data to/from a mobile device)
#
# The threads are started as daemons so they run in the background and terminate when the main program exits.
# =======================================================

import threading      # For running concurrent threads
import time           # For sleep control
import Serial_handling  # Module handling serial input/output with Arduinos
import mqtt_handler     # Module handling MQTT communication with mobile app

# -------------------------------------------------------
# Thread Starter Function
# -------------------------------------------------------
def start_threads():
    """
    Starts both the serial handling and MQTT communication threads.
    These run as background tasks to continuously:
        - Poll Arduino data
        - Update internal state
        - Publish/subscribe to MQTT topics
    """
    print("[MAIN] Starting serial and MQTT threads...")

    # Start the serial thread (for GPS, radar, control)
    serial_thread = threading.Thread(target=Serial_handling.serial_task, daemon=True)
    serial_thread.start()

    # Start the MQTT thread (for remote monitoring/control)
    mqtt_thread = threading.Thread(target=mqtt_handler.mqtt_task, daemon=True)
    mqtt_thread.start()

# -------------------------------------------------------
# Main Program Entry Point
# -------------------------------------------------------
if __name__ == "__main__":
    start_threads()  # Launch both threads

    # Keep the main thread alive to allow daemon threads to run
    try:
        while True:
            time.sleep(1)  # Sleep to prevent CPU overuse
    except KeyboardInterrupt:
        # Gracefully exit on Ctrl+C
        print("\n[MAIN] Program interrupted. Exiting...")
        pass
