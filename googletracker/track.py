import os, datetime, json, time
from locationsharinglib import Service
import paho.mqtt.client as mqtt
from geopy.distance import vincenty

email = os.environ['EMAIL']
password = os.environ['PASSWORD']
mqtt_server = os.environ['MQTT_SERVER']
poll_interval = os.environ['POLL_INTERVAL']
home_latitude = os.environ['HOME_LATITUDE']
home_longitude = os.environ['HOME_LONGITUDE']

print("Pulling locations for", email)

client = mqtt.Client()
client.connect(mqtt_server, 1883, 60)
client.loop_start()

print("Connected to", mqtt_server)

service = Service(email, password)

home = (float(home_latitude), float(home_longitude))

while True:
    for person in service.get_all_people():
        # ignore locations that are not at least accurate within 1000 meters
        if person._accuracy > 1000:
            continue
        mqtt_topic = 'google/location/' + person.full_name.lower().replace(" ","_")
        mqtt_data = {
            "latitude": person.latitude,
            "longitude": person.longitude,
            "datetime": int(person.timestamp),
            "accuracy": person._accuracy
        }

        # if home is within the accuracy radius, assume home
        if vincenty(home,(person.latitude, person.longitude)).meters < person._accuracy:
            mqtt_data["latitude"] = home[0]
            mqtt_data["longitude"] = home[1]
        
        print(mqtt_topic, mqtt_data)
        client.publish(mqtt_topic, json.dumps(mqtt_data), retain=True)

    time.sleep(float(poll_interval))
