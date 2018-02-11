FROM python:3.5

RUN pip3 install --no-cache-dir locationsharinglib paho-mqtt

COPY . .

CMD [ "python", "track.py" ]