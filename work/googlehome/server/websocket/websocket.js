#!/usr/bin/env node

var WebSocketServer = require('ws').Server;
var wss = new WebSocketServer({
	host: '0.0.0.0',
	port: 3000
});

var connections = new Array();
wss.on('connection', function(ws) {
	connections.push(ws);
	console.log("connected");
	ws.on('close', function () {
		connections = connections.filter(function (conn, i) {
			return (conn === ws) ? false : true;
		});
	});
	ws.on('message', function(message) {
		console.log('receive: %s', message);
		broadcast(message);
		
	});
});

function broadcast(message) {
	connections.forEach(function(con, i) {
		con.send(message);
	});
}
