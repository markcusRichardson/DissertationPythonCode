import paho.mqtt.client as mqtt
import configV  # Configuration file for global variables
import time
import threading

# MQTT Configuration
MQTT_BROKER = "localhost"  # Use the Raspberry Pi as the broker
MQTT_PORT = 1883
MQTT_TOPIC_LOCK = "bike/lock"
MQTT_TOPIC_BRIGHTNESS_FRONT = "bike/brightness/front"
MQTT_TOPIC_BRIGHTNESS_MIDDLE = "bike/brightness/middle"
MQTT_TOPIC_BRIGHTNESS_REAR = "bike/brightness/rear"
MQTT_TOPIC_MODE = "bike/mode"
MQTT_TOPIC_ALARM = "bike/alarm"
MQTT_TOPIC_GPS = "bike/gps"
MQTT_TOPIC_RADAR = "bike/radar"  # Added radar detection

# MQTT Client Setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("[MQTT] Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_LOCK)
    client.subscribe(MQTT_TOPIC_BRIGHTNESS_FRONT)
    client.subscribe(MQTT_TOPIC_BRIGHTNESS_MIDDLE)
    client.subscribe(MQTT_TOPIC_BRIGHTNESS_REAR)
    client.subscribe(MQTT_TOPIC_MODE)
    client.subscribe(MQTT_TOPIC_RADAR)  # Subscribe to radar topic

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"[MQTT] Message received on {topic}: {payload}")

    if topic == MQTT_TOPIC_LOCK:
        configV.lock_state = (payload == "lock")

    elif topic == MQTT_TOPIC_BRIGHTNESS_FRONT:
        configV.brightnessFront = int(payload)

    elif topic == MQTT_TOPIC_BRIGHTNESS_MIDDLE:
        configV.brightnessMiddle = int(payload)

    elif topic == MQTT_TOPIC_BRIGHTNESS_REAR:
        configV.brightnessRear = int(payload)

    elif topic == MQTT_TOPIC_MODE:
        configV.mode = int(payload)

    elif topic == MQTT_TOPIC_RADAR:  # Handling radar detection
        configV.radar_alert = (payload == "detected")
        print("[ALERT] Radar detected an object!")

def publish_alarm():
    print("[MQTT] Publishing alarm trigger!")
    client.publish(MQTT_TOPIC_ALARM, "ALARM TRIGGERED")

def publish_gps():
    if None in (configV.latitude, configV.longitude, configV.satellites):
        return
    gps_data = f"{configV.latitude},{configV.longitude},{configV.satellites}"
    print(f"[MQTT] Publishing GPS data: {gps_data}")
    client.publish(MQTT_TOPIC_GPS, gps_data)

def Check_alarm():
    if configV.alarm_bool:
        publish_alarm()
        publish_gps()

# Start the MQTT Loop
def mqtt_task():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()  # Runs in the background
     # Start Alarm Checking in a Separate Thread
    alarm_thread = threading.Thread(target=Check_alarm, daemon=True)
    alarm_thread.start()
