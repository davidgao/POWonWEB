#!/usr/bin/env python3

import json
import hashlib
import signal
import sys
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from threading import Thread


good_salts = ["good1", "good2"]
threshold = bytes.fromhex("7fffffff ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff")


def check_hash(h, threshold):
	for i in range(32):
		if h[i] > threshold[i]:
			return False
	return True


def handle_signal(signal, frame):
	server.stop()


class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		tmp = self.path.split(sep='?', maxsplit=1)
		path = tmp[0]
		args = {}
		for arg in tmp[1].split(sep='&'):
			kv = arg.split(sep='=')
			key = kv[0]
			val = kv[1]
			args[key] = val
		if path != "/echo":
			self.send_response(404)
			self.end_headers()
			addr, _ = self.client_address
			print("BAD GET %s from %s" % (path, addr))
		else:
			try:
				n = args.pop("nonce")
				s = args.pop("salt")
				h = bytes.fromhex(args.pop("hash"))
			except:
				print("BAD request length or format")
				self.send_response(400)
				self.end_headers()
				return
			req = json.dumps({
				"path": path,
				"args": args,
				"salt": s,
				"nonce": n,
			}).encode()
			
			# salt
			if s not in good_salts:
				print("BAD salt")
				self.send_response(400)
				self.end_headers()
				return
			# threshold
			if not check_hash(h, threshold):
				print("BAD hash")
				self.send_response(400)
				self.end_headers()
				return
			# hash
			h1 = hashlib.sha256()
			h1.update(req)
			h1 = h1.digest()
			h2 = hashlib.sha256()
			h2.update(h1)
			h2 = h2.digest()
			if h != h2:
				print("BAD nonce")
				self.send_response(400)
				self.end_headers()
				return
			self.send_response(200)
			self.end_headers()


class DemoHttpd(object):
	def __init__(self):
		super(DemoHttpd, self).__init__()
		self.thread = None
		
		self.httpd = HTTPServer(("", 8000), RequestHandler)
		
	def start(self):
		self.thread = Thread(target=self.httpd.serve_forever)
		self.thread.start()
	
	def stop(self):
		self.httpd.shutdown()
		self.thread.join()


server = DemoHttpd()
server.start()

signal.signal(signal.SIGINT, handle_signal)

