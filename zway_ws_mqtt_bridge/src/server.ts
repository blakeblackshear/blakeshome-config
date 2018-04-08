import * as WebSocket from 'websocket';
import * as http from 'http';
import * as MQTT from 'mqtt';

const server = http.createServer();
server.listen(9009, function() {
    console.log((new Date()) + ' Server is listening on port 9009');
});

const wss = new WebSocket.server({ httpServer: server });

const client = MQTT.connect(process.env.MQTT_SERVER);

let connection: WebSocket.connection;

wss.on('request', function(request) {
    connection = request.accept(undefined, request.origin);
    console.log((new Date()) + ' Connection accepted.');
    connection.on('message', function(message) {
        if (message.type === 'utf8' && message.utf8Data !== undefined) {
            let parsedMessage = JSON.parse(message.utf8Data);
            let retain = parsedMessage.deviceType === 'sensorDiscrete' ? false : true;
            let level = typeof parsedMessage.metrics.level !== 'undefined' ? parsedMessage.metrics.level : parsedMessage.metrics.lastLevel;
            if(typeof level !== 'undefined' && level !== '') {
                client.publish(`zway/${parsedMessage.id}/status`, level.toString(), { qos: 1, retain: retain});
            }
        }
    });
    connection.on('close', function(reasonCode, description) {
        console.log((new Date()) + ' Peer ' + connection.remoteAddress + ' disconnected.');
    });
});

client.on('connect', function() {
    console.log('MQTT Connected');
    client.subscribe('zway/+/set');
});

client.on('error', function(error) {
    console.log(`Error: ${error.message}`);
});

client.on('offline', function() {
    console.log('MQTT Offline');
});

client.on('close', function() {
    console.log('MQTT Closed');
});

client.on('message', function(topic, message) {
    if(connection){
        let topicParts = topic.split('/');
        let jsonMessage = {
            id: topicParts[1],
            command: topicParts[2],
            value: message.toString()
        };
        connection.sendUTF(JSON.stringify(jsonMessage));
    }
});