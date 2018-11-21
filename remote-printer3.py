#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Author: Carlos Garcia Gomez
# Date: 29-11-2013
# web: http://www.facturaScripts.com

import time, http.server, os
from urllib.request import urlopen
from subprocess import call

HOST_NAME = 'localhost'
PORT_NUMBER = 10080

class MyHandler(http.server.BaseHTTPRequestHandler):
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()

	def do_GET(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		
		global api_url
		extra_url = ''
		if len(s.path) > 2:
			extra_url = '&'+s.path[2:]
		response = urlopen(api_url+'?v=2&f=remote_printer'+extra_url)
		html = response.read()
		if html:
			f = open('ticket.txt', 'wb')
			f.write( html + b'\n' )
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
		api_url = input('URL de la api: ')
		printer_name = input('Nombre de la impresora: ')
		f = open('config.txt', 'w')
		f.write('api: '+api_url+"\nprinter: "+printer_name)
		f.close()

	# iniciamos el servidor web
	server_class = http.server.HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
	print( time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER) )
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print( time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER) )

	# borramos el ticket
	if os.path.isfile('ticket.txt'):
		os.remove('ticket.txt')
