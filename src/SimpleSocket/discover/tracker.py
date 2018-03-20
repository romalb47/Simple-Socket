#!/usr/bin/env python3
# coding: utf8

import xmlrpc.client

class Discover(object):
	def __init__(self, uri):
		self.uri = uri
		
	def init(self):
		pass
		
	def connect(self):
		self._proxy = xmlrpc.client.ServerProxy('http://'+self.uri)
		
	def announce(self, server_uid, service_uid, connection_list=[]):
		return self._proxy.announce(server_uid, service_uid, connection_list)
		
	def search(self, server_uid, service_uid):
		try:
			liste = self._proxy.search(server_uid, service_uid)
		except:
			return []
		return liste
		
	def close(self):
		pass
	
