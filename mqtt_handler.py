# ===============================================================
# Smart Bike System – MQTT Communication Handler
# ---------------------------------------------------------------
# This script uses the Paho MQTT client to handle communication
# between the Raspberry Pi and external devices (e.g., smartphone app).
# It supports:
#   - Receiving control commands (lock, brightness, mode, alarm reset)
#   - Publishing live telemetry data (GPS, speed, radar, etc.)
#   - Notifying on alarm activation
# ===============================================================

import paho.mqtt.client as mqtt    # MQTT library
import configV                     # Shared configuration values
import time                        # For timing/publishing intervals
import threading                   # For concurrent background tasks

# ---------------------------------------------------------------
# MQTT Configuration
# ---------------------------------------------------------------
BROKER = "localhost"  # MQTT broker (change if remote or cloud-based)
PORT = 1883

# Topics dictionary for consistency and maintainability
TOPICS = {
    "LOCK": "bike/lock",
    "BRIGHTNESS_FRONT": "bike/brightness/front",
    "BRIGHTNESS_MIDDLE": "bike/brightness/middle",
    "BRIGHTNESS_REAR": "bike/brightness/rear",
    "BRIGHTNESS_LOGO": "bike/brightness/logo",
    "MODE": "bike/mode",
    "ALARM": "bike/alarm",
    "RADAR": "bike/radar",
    "LONGITUDE": "bike/longitude",
    "LATITUDE": "bike/latitude",
    "SPEED": "bike/speed",
    "SATELLITES": "bike/satellites",
    "ALTITUDE": "bike/altitude",
    "RADAR_READING": "bike/radar_reading",
    "ALARM_BOOL_RESET": "bike/alarmReset",
}

# Create MQTT client instance
client = mqtt.Client()

# ---------------------------------------------------------------
# Callback: On Connection to Broker
# ---------------------------------------------------------------
def on_connect(client, userdata, flags, rc):
    """
    Subscribes to relevant topics upon connecting to the MQTT broker.
    Ensures subscriptions are re-applied after reconnections.
    """
    for topic in TOPICS.values():
        client.subscribe(topic)

# ---------------------------------------------------------------
# Callback: On Receiving MQTT Messages
# ---------------------------------------------------------------
def on_message(client, userdata, msg):
    """
    Handles incoming MQTT messages and updates shared configuration
    values accordingly to influence system behavior.
    """
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

# ---------------------------------------------------------------
# Publish Alarm Notification
# ---------------------------------------------------------------
def publish_alarm():
    """
    Publishes an alert message to notify that the alarm condition is active.
    """
    client.publish(TOPICS["ALARM"], "ALARM TRIGGERED")

# ---------------------------------------------------------------
# Alarm Monitoring Loop
# ---------------------------------------------------------------
def check_alarm():
    """
    Continuously checks if the alarm has been triggered
    and publishes a notification when necessary.
    """
    while True:
        if configV.alarm_bool:
            publish_alarm()
        time.sleep(0.1)

# ---------------------------------------------------------------
# Callback: On Disconnection
# ---------------------------------------------------------------
def on_disconnect(client, userdata, rc):
    """
    Attempts to reconnect if the MQTT connection is lost.
    """
    try:
        client.reconnect()
    except Exception as err:
        pass  # Optional: log error

# ---------------------------------------------------------------
# Sensor Data Publishing Loop
# ---------------------------------------------------------------
def publish_sensor_data():
    """
    Publishes telemetry data (e.g., GPS, speed, radar) to MQTT topics every second.
    Also interprets radar reading values into descriptive messages.
    """
    while True:
        # Gather values to publish
        speed = str(configV.speed)
        latitude = str(configV.latitude)
        longitude = str(configV.longitude)
        satellites = str(configV.satellites)
        altitude = str(configV.altitude)
        radar = str(configV.segments)
        radar_reading = configV.radar_reading

        # Publish each value
        client.publish(TOPICS["SPEED"], speed)
        client.publish(TOPICS["RADAR"], radar)
        client.publish(TOPICS["LONGITUDE"], longitude)
        client.publish(TOPICS["LATITUDE"], latitude)
        client.publish(TOPICS["ALTITUDE"], altitude)
        client.publish(TOPICS["SATELLITES"], satellites)

        # Determine radar state and publish human-readable message
        if radar_reading == 1:
            configV.radar_output = "Approaching Detected"
        elif radar_reading == 2:
            configV.radar_output = "Departing Detected"
        elif radar_reading == 3:
            configV.radar_output = "Sustained approach"
        elif radar_reading == 4:
            configV.radar_output = "Sustained away"
        else:
            configV.radar_output = "No Detection"

        client.publish(TOPICS["RADAR_READING"], configV.radar_output)
        time.sleep(1)  # Publish interval

# ---------------------------------------------------------------
# Main MQTT Task Function (Entry Point for Thread)
# ---------------------------------------------------------------
def mqtt_task():
    """
    Initializes MQTT client, connects to the broker, and starts the message loop.
    Launches two threads:
        - One to monitor the alarm state
        - One to periodically publish sensor data
    """
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect(BROKER, PORT, 60)
    client.loop_start()  # Starts non-blocking loop in background

    # Background threads for alarm and telemetry
    threading.Thread(target=check_alarm, daemon=True).start()
    threading.Thread(target=publish_sensor_data, daemon=True).start()
