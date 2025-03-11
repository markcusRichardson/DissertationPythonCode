import paho.mqtt.client as mqtt



# MQTT variables
MQTT_BROKER = "IP Address"
MQTT_PORT = 1883
MQTT_TOPIC_SUBSCRIBE = "bike/control"
MQTT_TOPIC_PUBLISH = "bike/data"
client = mqtt.Client()

