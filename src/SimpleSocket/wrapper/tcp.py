#!/usr/bin/env python3
# coding: utf8

class Client(object):
	
	def __init__(self, uri):
		self.uri = uri
		self.is_connected = False
		
	def init(self):
		pass
		
	def connect(self):
		pass
		
	def connect_fast(self):
		pass
		
	def refresh(self):
		pass

	def send(self, priority, data):
		pass

	def recv(self):
		pass
		
	def loop(self):
		pass
		
	def close(self):
		pass

class Server(object):
	
	def __init__(self, uri):
		self.uri = uri
		self.is_connected = False
		
	def init(self):
		pass
		
	def listen(self):
		pass

	def send(self, priority, data):
		pass

	def recv(self):
		pass

	def loop(self):
		pass
		
	def close(self):
		pass
