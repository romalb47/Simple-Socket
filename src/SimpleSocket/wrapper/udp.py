#!/usr/bin/env python3
# coding: utf8

import socket
import sys

class Client(object):
	
	def __init__(self, uri):
		self.uri = uri
		self.last_message = 0
		self.is_connected = False
		
	def init(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		socket_addr = self.uri.split(":")
		if len(socket_addr)==1:
			self.port = 9876
		else:
			self.port = int(socket_addr[1])
		self.addr = str(socket_addr[0])
		self.server_address = (self.addr, self.port)
		
		self.sock.setblocking(0)
		
	def connect(self):
		self.sock.sendto(b'Cconnect', self.server_address)
		
	def connect_fast(self):
		self.sock.sendto(b'Cconnect', self.server_address)
		
	def refresh(self):
		self.sock.sendto(b'Cping', self.server_address)

	def send(self, priority, data):
		data = b"D" + bytes([priority]) + bytes(message)
		self.sock.sendto(message, server_address)

	def recv(self):
		try:
			data, server = self.sock.recvfrom(4096)
		except socket.timeout:
			return None, None
		
		self.last_message = time.time()
		
		if data.startswith(b'D'):
			return data[1], data[2:]
			
		if data.startswith(b'C'):
			if data == b"Caccepted":
				self.is_connected = True
			if data == b"Cpong":
				self.is_connected = True
			
		return None, None
		
	def loop(self):
		pass
		
	def close(self):
		self.sock.close()

class Server(object):
	
	def __init__(self, uri):
		self.uri = uri
		self.last_message = 0
		self.is_connected = False
		
	def init(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		socket_addr = self.uri.split(":")
		if len(socket_addr)==1:
			self.port = 9876
		else:
			self.port = int(socket_addr[1])
		self.addr = str(socket_addr[0])
		self.server_address = (self.addr, self.port)
		
		self.sock.setblocking(0)
		
	def listen(self):
		self.sock.bind(self.server_address)
		
	def refresh(self):
		self.sock.sendto(b'Cping', self.server_address)

	def send(self, priority, data):
		data = b"D" + bytes([priority]) + bytes(message)
		self.sock.sendto(message, server_address)

	def recv(self):
		try:
			data, server = self.sock.recvfrom(4096)
		except socket.timeout:
			return None, None
		
		self.last_message = time.time()
		
		if data.startswith(b'D'):
			return data[1], data[2:]
			
		if data.startswith(b'C'):
			if data == b"Caccepted":
				self.is_connected = True
			if data == b"Cpong":
				self.is_connected = True
			
		return None, None
		
	def loop(self):
		pass
		
	def close(self):
		self.sock.close()
