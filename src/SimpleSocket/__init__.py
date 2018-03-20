#!/usr/bin/env python3
# coding: utf8

import threading, queue, time
import uuid, socket, hashlib
import importlib

from . import utils


class ClientSocket(object):
	
	
	def __init__(self, service_uid, server_uid=None, queue_size=1024, discovery_protocole=["tracker://127.0.0.1:8000"]):
		self._discovery_protocole = discovery_protocole
		self._queue_size = queue_size
		self._queue_in = queue.PriorityQueue(maxsize=self._queue_size)
		self._queue_out = queue.PriorityQueue(maxsize=self._queue_size)
		self.service_uid = service_uid
		self._thread = None
		self.is_connected = False
		self._stop_thread = False
		
		if not server_uid:
			self.server_uid = hex(uuid.getnode())
		else:
			self.server_uid = str(server_uid)

	def start_loop(self):
		self.stop_thread = False
		self.is_connected = False
		self.thread = threading.Thread(target=self.run_loop)
		self.thread.start()
		
	def stop_loop(self, timeout=None):
		self.stop_thread = True
		self.thread.join(timeout)
		
	def recv_data(self, timeout=1):
		if timeout==0:
			return self._queue_in.get(False)[1]
		else:
			return self._queue_in.get(True, timeout)[1]
		
	def send_data(self, data, priority=10):
		self._queue_out.put_nowait( (priority, data) )
	
	def run_loop(self):
		connected_socket = 0				
		discover_module = []
				
		connection_list = set()
				
		for proto in self._discovery_protocole:
			module = proto.split("://")[0]
			m = importlib.import_module("SimpleSocket.discover."+str(module))
			discover_module.append(m.Discover(proto.split("://", 1)[1]))

		for discover in discover_module:
			discover.init()
			
		for discover in discover_module:
			discover.connect()

		while not self._stop_thread:
			
			for discover in discover_module:
				utils.each(connection_list.add, discover.search(self.server_uid, self.service_uid))
			print("Liste de connexion: "+str(connection_list))
			
			connection_wrapper = self.get_connection(connection_list)
			
			while connected_socket > 0:
				
				for connection in connection_wrapper:
					if connection.is_connected:
						data = connection.loop()
						self.parse_data(data, connection)
						
				for connection in connection_wrapper:
					if connection.is_connected:
						try:
							priority, data = self._queue_out.get_nowait()
						except queue.Empty:
							pass
						else:
							connection.send(priority, data)
						finally:
							break

				connected_socket = self.refresh_connection(connection_wrapper)
				time.sleep(5)

			
			time.sleep(5)

	def get_connection(self, uri_list):
		
		connected_socket = 0
			
		wrapper_module = []
				
		for proto in uri_list:
			module = proto.split("://")[0]
			m = importlib.import_module("SimpleSocket.wrapper."+str(module))
			wrapper_module.append(m.Client(proto.split("://", 1)[1]))

		for wrapper in wrapper_module: #TODO Parser les IPs afin de prioritiser les locals
			wrapper.init()
			
		for wrapper in wrapper_module:
			wrapper.connect()
			if wrapper.is_connected == True:
				connected_socket += 1
			
			if connected_socket > 1:
				break

		return wrapper_module
		
	def refresh_connection(self, wrapper_module):
		
		connected_socket = 0
		for wrapper in wrapper_module:
			if wrapper.is_connected == True:
				wrapper.refresh()
				connected_socket += 1
			
		if connected_socket > 1:
			for wrapper in wrapper_module:
				if wrapper.is_connected == False:
					wrapper.connect_fast()
				if wrapper.is_connected == True:
					connected_socket += 1
				
				if connected_socket > 1:
					break

		return connected_socket

	def parse_data(self, data, connection): # Mets en queue_in les données
		pass
