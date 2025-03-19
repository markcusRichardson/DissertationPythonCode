import paho.mqtt.client as mqtt
import configV  # Configuration file for global variables
import time

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

# MQTT Client Setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    # Subscribe to Topics
    client.subscribe(MQTT_TOPIC_LOCK)
    client.subscribe(MQTT_TOPIC_BRIGHTNESS_FRONT)
    client.subscribe(MQTT_TOPIC_BRIGHTNESS_MIDDLE)
    client.subscribe(MQTT_TOPIC_BRIGHTNESS_REAR)
    client.subscribe(MQTT_TOPIC_MODE)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    if topic == MQTT_TOPIC_LOCK:
        if payload == "lock":
            configV.lock_state = True
        elif payload == "unlock":
            configV.lock_state = False

    elif topic == MQTT_TOPIC_BRIGHTNESS_FRONT:
        configV.brightnessFront = int(payload)

    elif topic == MQTT_TOPIC_BRIGHTNESS_MIDDLE:
        configV.brightnessMiddle = int(payload)

    elif topic == MQTT_TOPIC_BRIGHTNESS_REAR:
        configV.brightnessRear = int(payload)

    elif topic == MQTT_TOPIC_MODE:
        configV.mode = int(payload)

def publish_alarm():
    client.publish(MQTT_TOPIC_ALARM, "ALARM TRIGGERED")

def publish_gps():
    if configV.latitude is None or configV.longitude is None or configV.satellites is None:
        return
    gps_data = f"{configV.latitude},{configV.longitude},{configV.satellites}"
    client.publish(MQTT_TOPIC_GPS, gps_data)


# Start the MQTT Loop
def mqtt_task():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    if configV.alarm_bool == True:
        publish_alarm()
        publish_gps()
        time.sleep(0.1)




