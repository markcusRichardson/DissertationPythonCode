import paho.mqtt.client as mqtt
import configV  # Configuration file for global variables
import time
import threading

# MQTT Configuration
BROKER = "localhost"
PORT = 1883
TOPICS = {
    "LOCK": "bike/lock",
    "BRIGHTNESS_FRONT": "bike/brightness/front",
    "BRIGHTNESS_MIDDLE": "bike/brightness/middle",
    "BRIGHTNESS_REAR": "bike/brightness/rear",
    "MODE": "bike/mode",
    "ALARM": "bike/alarm",
    "GPS": "bike/gps",
    "RADAR": "bike/radar",
}

# MQTT Client Setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    """Handles MQTT connection and re-subscribes to topics."""
    print("Connected mate")
    if rc == 0:
        print("[MQTT] Connected Successfully!")
    else:
        print(f"[MQTT] Connection failed with code {rc}")

    # ✅ Ensure re-subscription after reconnection
    for topic in TOPICS.values():
        client.subscribe(topic)

def on_message(client, userdata, msg):
    """Processes incoming MQTT messages."""
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"[MQTT] Received on {topic}: {payload}")

    if topic == TOPICS["LOCK"]:
        configV.lock_state = (payload == "lock")

    elif topic == TOPICS["BRIGHTNESS_FRONT"]:
        print(f"[DEBUG] Before: {configV.brightnessFront}")
        configV.brightnessFront = int(payload)
        print(f"[DEBUG] After: {configV.brightnessFront}")

    elif topic == TOPICS["BRIGHTNESS_MIDDLE"]:
        configV.brightnessMiddle = int(payload)

    elif topic == TOPICS["BRIGHTNESS_REAR"]:
        configV.brightnessRear = int(payload)

    elif topic == TOPICS["MODE"]:
        configV.mode = int(payload)

    elif topic == TOPICS["RADAR"]:
        configV.radar_alert = (payload == "detected")
        print("[ALERT] Radar detected an object!")

def publish_alarm():
    result = client.publish(TOPICS["ALARM"], "ALARM TRIGGERED")
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print("[MQTT] Alarm Published!")
    else:
        print("[MQTT] Failed to Publish Alarm!")

def publish_gps():
    """Publishes GPS data."""
    if None in (configV.latitude, configV.longitude, configV.satellites):
        return
    gps_data = f"{configV.latitude},{configV.longitude},{configV.satellites}"
    result = client.publish(TOPICS["GPS"], gps_data)
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
    """Handles MQTT disconnection and attempts one reconnect."""
    print(f"[MQTT] Disconnected with result code {rc}")
    try:
        client.reconnect()
        print("[MQTT] Reconnected Successfully!")
    except Exception as err:
        print(f"[MQTT] Reconnect Failed: {err}")

# Start the MQTT Loop
def mqtt_task():
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect  
    client.connect(BROKER, PORT, 60)
    print("Running MQTT handler")
    client.loop_start()  

    # ✅ Start alarm checking in a separate thread
    threading.Thread(target=check_alarm, daemon=True).start()
