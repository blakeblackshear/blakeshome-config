FROM python:3.5

RUN pip3 install --no-cache-dir locationsharinglib==0.3.0 paho-mqtt geopy

COPY . .

CMD [ "python", "track.py" ]