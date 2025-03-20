import paho.mqtt.client as mqtt
import configV  # Configuration file for global variables
import time
import threading

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_LOCK = "bike/lock"
MQTT_TOPIC_BRIGHTNESS_FRONT = "bike/brightness/front"
MQTT_TOPIC_BRIGHTNESS_MIDDLE = "bike/brightness/middle"
MQTT_TOPIC_BRIGHTNESS_REAR = "bike/brightness/rear"
MQTT_TOPIC_MODE = "bike/mode"
MQTT_TOPIC_ALARM = "bike/alarm"
MQTT_TOPIC_GPS = "bike/gps"
MQTT_TOPIC_RADAR = "bike/radar"

# MQTT Client Setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    """Handles successful MQTT connection and re-subscribes to topics."""
    if rc == 0:
        print("[MQTT] Connected Successfully!")
    else:
        print(f"[MQTT] Connection failed with code {rc}")

    # ✅ Ensure re-subscription after reconnection
    client.subscribe(MQTT_TOPIC_LOCK)
    client.subscribe(MQTT_TOPIC_BRIGHTNESS_FRONT)
    client.subscribe(MQTT_TOPIC_BRIGHTNESS_MIDDLE)
    client.subscribe(MQTT_TOPIC_BRIGHTNESS_REAR)
    client.subscribe(MQTT_TOPIC_MODE)
    client.subscribe(MQTT_TOPIC_RADAR)

def on_message(client, userdata, msg):
    """Processes incoming MQTT messages."""
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"[MQTT] Received on {topic}: {payload}")

    if topic == MQTT_TOPIC_LOCK:
        configV.lock_state = (payload == "lock")

    elif topic == MQTT_TOPIC_BRIGHTNESS_FRONT:
        print(f"[DEBUG] Before: {configV.brightnessFront}")
        configV.brightnessFront = int(payload)
        print(f"[DEBUG] After: {configV.brightnessFront}")
        configV.display_update_needed = True  # ✅ Notify GUI of updates

    elif topic == MQTT_TOPIC_BRIGHTNESS_MIDDLE:
        configV.brightnessMiddle = int(payload)

    elif topic == MQTT_TOPIC_BRIGHTNESS_REAR:
        configV.brightnessRear = int(payload)

    elif topic == MQTT_TOPIC_MODE:
        configV.mode = int(payload)

    elif topic == MQTT_TOPIC_RADAR:
        configV.radar_alert = (payload == "detected")
        print("[ALERT] Radar detected an object!")

def publish_alarm():
    """Publishes an alarm trigger message."""
    result = client.publish(MQTT_TOPIC_ALARM, "ALARM TRIGGERED")
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print("[MQTT] Alarm Published!")
    else:
        print("[MQTT] Failed to Publish Alarm!")

def publish_gps():
    """Publishes GPS data."""
    if None in (configV.latitude, configV.longitude, configV.satellites):
        return
    gps_data = f"{configV.latitude},{configV.longitude},{configV.satellites}"
    result = client.publish(MQTT_TOPIC_GPS, gps_data)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"[MQTT] GPS Data Published: {gps_data}")
    else:
        print("[MQTT] Failed to Publish GPS Data!")

def check_alarm():
    """Continuously checks if the alarm should be triggered."""
    while True:
        if configV.alarm_bool:
            publish_alarm()
            publish_gps()
        time.sleep(0.1)

def on_disconnect(client, userdata, rc):
    """Handles disconnection and automatic reconnection."""
    print(f"[MQTT] Disconnected with result code {rc}")
    while True:
        try:
            client.reconnect()
            print("[MQTT] Reconnected Successfully!")
            return
        except Exception as err:
            print(f"[MQTT] Reconnect Failed: {err}")
        time.sleep(5)  # Wait before retrying

# Start the MQTT Loop
def mqtt_task():
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect  # ✅ Automatic reconnects
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()  # ✅ Runs MQTT in the background

    # ✅ Start the alarm check in a separate thread
    alarm_thread = threading.Thread(target=check_alarm, daemon=True)
    alarm_thread.start()
