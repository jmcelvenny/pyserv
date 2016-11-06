#!/usr/bin/python

import socket
import sys
import os
import os.path
import time
import signal
from importlib import import_module

def signal_handler(signal, frame):
        sys.exit(0)

def onPageLoad(params):
	return "nice try"

def sendWriteHeaders(sock, lastmodified, contenttype, clen):
	sock.send("Server: pyserv\n")
	sock.send("Date: " + time.strftime("%c") + "\n")
	sock.send("Last-Modified: " + lastmodified + "\n")
	sock.send("Content-Type: " + contenttype + "\n")
	sock.send("Content-Length: " + str(clen) + "\n")
	sock.send("Connection: close\n\n")

def sendErrorPageAndClose(conn, errmsg, httpcode):
	errmsg = str(httpcode) + " " + errmsg
	conn.send("HTTP/1.1 " + str(httpcode) + " " + errmsg)
	sendWriteHeaders(conn, time.strftime("%c"), "text/html", len(errmsg))
	conn.send(errmsg)
	conn.close()

def isInteger(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def main():
	signal.signal(signal.SIGINT, signal_handler)
	if (len(sys.argv) != 3):
		print "Usage: python server.py <PORTNO> <HOST>"
		sys.exit()

	if (isInteger(sys.argv[1]) == False):
		print "Argument must be an integer! Given: %s" % sys.argv[1]
		sys.exit()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = sys.argv[2]
	port = int(sys.argv[1])

	try:
		s.bind((host, port))
	except socket.error as msg:
		print "Call to bind failed. Error Code: %d. Message: %s" % (msg[0], msg[1])
		sys.exit()

	print "Server running on %s %s " % (host, port)
	s.listen(5) #five backlogged connections allowed
	while True:
		#connection object, address object
		conn, addr = s.accept()
		data = conn.recv(1024) #url/req
		if (data == ""):
			continue

		parts = data.split();

		if (len(parts) < 3):
			print "Received connection from: %s: %s" % (addr, parts)
			sendErrorPageAndClose(conn, "Bad Request", 400)
			continue

		print "Received connection from: %s: %s %s %s" % (addr, parts[0], parts[1], parts[2])

		if (parts[0] != "GET"):
			sendErrorPageAndClose(conn, "Unsupported Method", 405)

		if (parts[2] != "HTTP/1.1"):
			sendErrorPageAndClose(conn, "Bad Request", 400)

		f = parts[1]

		if (f[-1:] == "/"):
			f = f + "index.html"

		tree = f.split("/")
		file_and_params = tree[len(tree)-1]
		filename = file_and_params.split("?")[0]
		parameters = ""
		if ("?" in file_and_params):
			parameters = file_and_params.split("?")[1]

		fpath = f.split("?")[0]

		#1
		if (fpath[0] == "/"):
			fpath = fpath[1:]

		if (os.path.isfile(fpath)):
			if (os.access(fpath, os.R_OK)):
				if (filename == "__init__.py"):
					sendErrorPageAndClose(conn, "Not Found", 404)
					continue
					
				if (filename[-3:] == ".py"):
					try:
						module = import_module(fpath[:-3].replace("/","."))
						pydata = module.onPageLoad(parameters)
						conn.send("HTTP/1.1 200 OK\n")
						sendWriteHeaders(conn, time.strftime("%c"), "text/html", len(pydata))
						conn.send(pydata)
						continue
					except ImportError:
						print "Module %s did not contain onPageLoad. Displaying error." % fpath
						sendErrorPageAndClose(conn, "Internal Error", 500)
						continue
				elif (filename[-4:] == ".pyc"):
					#sometimes the .pyc files can contain sensitive stuff
					#so it's best to just say they don't exist
					sendErrorPageAndClose(conn, "Not Found", 404)
				else:
					f = open(fpath, 'r')
					filedata = f.read()
					conn.send("HTTP/1.1 200 OK\n")
					sendWriteHeaders(conn, time.ctime(os.stat(fpath).st_mtime), "text/html", len(filedata))
					conn.send(filedata)
			else:
				sendErrorPageAndClose(conn, "Forbidden", 403)
		elif (os.path.isdir(fpath)):
			fpath = fpath + "/index.html"
			if (os.path.isfile(fpath)):
				if (os.access(fpath, os.R_OK)):
					f = open(fpath, 'r')
					filedata = f.read()
					conn.send("HTTP/1.1 200 OK\n")
					sendWriteHeaders(conn, time.ctime(os.stat(fpath).st_mtime), "text/html", len(filedata))
					conn.send(filedata)
				else:
					sendErrorPageAndClose(conn, "Forbidden", 403)
			else:
				sendErrorPageAndClose(conn, "Folder Exists; Index Not Found", 404)
		else:
			sendErrorPageAndClose(conn, "Not Found", 404)


main()