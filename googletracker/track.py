import os, datetime, json, time
from locationsharinglib import Service
import paho.mqtt.client as mqtt

email = os.environ['EMAIL']
password = os.environ['PASSWORD']
mqtt_server = os.environ['MQTT_SERVER']
poll_interval = os.environ['POLL_INTERVAL']

print("Pulling locations for", email)

client = mqtt.Client()
client.connect(mqtt_server, 1883, 60)
client.loop_start()

print("Connected to", mqtt_server)

service = Service(email, password)

while True:
    for person in service.get_all_people():
        mqtt_topic = 'google/location/' + person.full_name.lower().replace(" ","_")
        mqtt_data = {
            "latitude": person.latitude,
            "longitude": person.longitude,
            "datetime": int(person.datetime.timestamp())
        }
        
        print(mqtt_topic, mqtt_data)
        client.publish(mqtt_topic, json.dumps(mqtt_data), retain=True)

    time.sleep(float(poll_interval))
