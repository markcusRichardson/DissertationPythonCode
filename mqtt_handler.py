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
    "BRIGHTNESS_LOGO": "bike/brightness/logo ",
    "MODE": "bike/mode",
    "ALARM": "bike/alarm",
    "GPS": "bike/gps",
    "RADAR": "bike/radar",
    "RADAR_READING": "bike/radar_reading",
    "ALARM_BOOL_RESET": "bike/alarmReset",
}
  
# MQTT Client Setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    # Ensure re-subscription after reconnection
    for topic in TOPICS.values():
        client.subscribe(topic)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    if topic == TOPICS["LOCK"]:
        configV.lock_state = payload == "1"  
        
    elif topic == TOPICS["BRIGHTNESS_FRONT"]:
        configV.brightnessFront = int(payload)

    elif topic == TOPICS["BRIGHTNESS_MIDDLE"]:
        configV.brightnessMiddle = int(payload)

    elif topic == TOPICS["BRIGHTNESS_REAR"]:
        configV.brightnessRear = int(payload)
    
    elif topic == TOPICS["BRIGHTNESS_LOGO"]:
        configV.brightnessLogo = int(payload)
        
    elif topic == TOPICS["MODE"]:
        configV.mode = int(payload)

    elif topic == TOPICS["ALARM_BOOL_RESET"]:
        configV.alarm_bool_reset = payload == "1" 

def publish_alarm():
    result = client.publish(TOPICS["ALARM"], "ALARM TRIGGERED")


def check_alarm():
    while True:
        if configV.alarm_bool:
            publish_alarm()
        time.sleep(0.1)

def on_disconnect(client, userdata, rc):
    try:
        client.reconnect()
    except Exception as err:
        pass

def publish_sensor_data():
    while True:
        speed = configV.speed
        gps_data = f"{configV.latitude},{configV.longitude},{configV.satellites}, {configV.altitude}"
        radar = configV.segments
        radar_reading=configV.radar_reading
        radar_output = configV.radar_output
        client.publish(TOPICS["SPEED"], speed)
        client.publish(TOPICS["RADAR"], radar)
        client.publish(TOPICS["GPS"], gps_data)
        if radar_reading == 1:
            configV.radar_output == "Approaching Detected"
            client.publish(TOPICS["RADAR_READING"], radar_output)
        elif radar_reading == 2:
            configV.radar_output == "Departing Detected"
            client.publish(TOPICS["RADAR_READING", radar_output])
        elif radar_reading == 3:
            configV.radar_output == "Sustained approach"
            client.publish(TOPICS["RADAR_READING", radar_output])
        elif radar_reading == 4:
            configV.radar_output == "Sustained away"
            client.publish(TOPICS["RADAR_READING", radar_output])
        else :
            configV.radar_output = ""

        time.sleep(1)  

# Start the MQTT Loop
def mqtt_task():
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect  
    client.connect(BROKER, PORT, 60)
    client.loop_start()  

    # Start alarm checking in a separate thread
    threading.Thread(target=check_alarm, daemon=True).start()
    threading.Thread(target=publish_sensor_data, daemon=True).start()
