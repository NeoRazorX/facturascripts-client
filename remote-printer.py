#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Author: Carlos Garcia Gomez
# Date: 29-11-2013
# web: http://www.facturaScripts.com

import time, BaseHTTPServer, urllib2, os
from subprocess import call

HOST_NAME = 'localhost'
PORT_NUMBER = 10080

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()

	def do_GET(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		
		global api_url
		response = urllib2.urlopen(api_url+'?remote-printer=TRUE')
		html = response.read()
		if html != '':
			f = open('ticket.txt', 'w')
			f.write(html+"\n")
			f.close()
			global printer_name
			call(['lpr', '-P', printer_name, 'ticket.txt'])

if __name__ == '__main__':
	# preguntamos por la configuración
	global api_url
	global printer_name
	if os.path.isfile('config.txt'):
		f = open('config.txt', 'r')
		line = f.readline()
		api_url = line[5:].rstrip()
		line = f.readline()
		printer_name = line[9:].rstrip()
		f.close()
	else:
		api_url = raw_input('URL de la api: ')
		printer_name = raw_input('Nombre de la impresora: ')
		f = open('config.txt', 'w')
		f.write('api: '+api_url+"\nprinter: "+printer_name)
		f.close()

	# iniciamos el servidor web
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

	# borramos el ticket
	if os.path.isfile('ticket.txt'):
		os.remove('ticket.txt')