#!/usr/bin/python

import websocket
import thread

import os
import cgi
import cgitb

cgitb.enable()

if 'QUERY_STRING' in os.environ:
    query = cgi.parse_qs(os.environ['QUERY_STRING'])
else:
    query = {}

print "Content-Type: application/json\n\n"
print '{"status": "OK"}'


websocket.enableTrace(True)
ws = websocket.WebSocket()
ws.connect("ws://localhost:3000/ws")
ws.send('arm_and_takeoff')
