import * as WebSocket from 'ws';
import * as http from 'http';
import * as MQTT from 'mqtt';
import {URL} from 'url';

const client = MQTT.connect(process.env.MQTT_SERVER);

const wss = new WebSocket.Server({ port: 9009 });

const wsMap = new Map<string,WebSocket>();

wss.on('connection', function connection(ws, req){
    let device_id: string;
    console.log((new Date()) + ' - Connection accepted.');

    ws.on('message', (message) => {
        let stringMessage = message.toString();
        // if the message is not JSON, store it as the device_id
        if(stringMessage[0] !== '{'){
            console.log(`Device id: ${stringMessage}`);
            device_id = stringMessage;
            wsMap.set(stringMessage,ws);
            return;
        }

        // ignore messages until a device_id has been received
        if(device_id == null) { return; }

        // parse json message and send an MQTT message
        let parsedMessage = JSON.parse(stringMessage);
        let retain = parsedMessage.deviceType === 'sensorDiscrete' ? false : true;
        let level = parsedMessage.metrics.level ? parsedMessage.metrics.level : parsedMessage.metrics.lastLevel;
        if(typeof level !== 'undefined' && level !== '') {
            client.publish(`zwave/${device_id}/${parsedMessage.id}/status`, level.toString(), { qos: 1, retain: retain});
        }
    });

    ws.on('close', () => wsMap.delete(device_id));
});

client.on('message', (topic, message) => {
    console.log(`${topic} - ${message}`);
    let topicParts = topic.split('/');
    let device_id = topicParts[1];
    let jsonMessage = {
        id: topicParts[2],
        command: topicParts[3],
        value: message.toString()
    };

    let ws = wsMap.get(device_id);
    if(ws === undefined){
        console.log(`No websocket connection for ${device_id}`);
        return;
    }

    ws.send(JSON.stringify(jsonMessage));
});

client.on('connect', () => {
    console.log('MQTT Connected');
    client.subscribe('zwave/+/+/set');
});
