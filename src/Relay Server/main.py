#!/usr/bin/env python3
# coding: utf8

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

SERVICE_ANNOUNCE = {"0x363436383836#toto": ["tcp://tata.com:5445"], "0xa4173116772e#toto": ["tcp://tato.com:5445"]}

# Create server
server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=SimpleXMLRPCRequestHandler)
server.register_introspection_functions()

server.register_function(pow)

# Register a function under a different name
def announce(server_uid, service_uid, connection_list):
	key = str(server_uid) + "#" + str(service_uid)
	SERVICE_ANNOUNCE[key] = list(connection_list)
	print("Set key: " + key)
	return True
		
server.register_function(announce)

# Register a function under a different name
def search(server_uid, service_uid):
	key = str(server_uid) + "#" + str(service_uid)
	print("Ask key: "+key)
	return SERVICE_ANNOUNCE.get(key, [])
				
server.register_function(search)

	# Run the server's main loop
server.serve_forever()

