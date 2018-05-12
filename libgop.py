#!/usr/bin/env python
import socket
#libgop gopher library.
import io
import tempfile
import sys


stopget=0
print("libgop gopher library v0.1")
print("check python version...")
vers=sys.version_info[0]
if vers==2:
	print("Python 2")
else:
	print("python 3")
class mitem:
	def __init__(self, data, txtflg=0):
		if not isinstance(data, str) and vers==3:
			data=data.decode()
			#print("py3 data convert")
		if txtflg:
			self.datalist=None
			self.hostname=None
			self.selector=None
			self.gtype=None
			data=data.replace("\r\n", "").replace("\t", "        ")
			self.name=data
		else:
				
			try:
				
				self.gtype=data[0]
				self.datalist=data[1:].split("\t")
				self.name=self.datalist[0]
				self.selector=self.datalist[1]
				self.hostname=self.datalist[2]
				self.port=self.datalist[3]
			except IndexError:
				self.datalist=None
				self.hostname=None
				self.selector=None
				self.gtype=None
				data=data.replace("\r\n", "").replace("\t", "        ")
				self.name=data


def menudecode(data, txtflg=0):
	menulist=[]
	for item in data:
		menulist.extend([mitem(item, txtflg)])
	return menulist
#gopherget uses tempfile as a buffer.
#if stopget is set to 1 while gopherget is reciving data, it will abruptly stop. subsequent calls will reset stopget.
#if stopget is set to 2, both active and subsequent calls will imediately stop. the latter is used upon Zoxenpher shutting down.
def gopherget(host, port, selector, query=None):
	global stopget
	if stopget==1:
		stopget=0
	print("GopherGet: \"" + host + ":" + str(port) + " " + selector + "\"")
	gsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	gsocket.connect((host, int(port)))
	if query!=None:
		query="\t"+query
	else:
		query=""
	if vers==2:
		gsocket.sendall(""+(selector)+query+'\r\n')
	else:
		gsocket.sendall((""+(selector)+query+'\r\n').encode("utf-8"))
	x = gsocket.recv(1024)
	tmpbuff=tempfile.TemporaryFile("r+b")
	while (x) and stopget==0:
		print("Receiving...")
		tmpbuff.write(x)
		x = gsocket.recv(1024)
	if stopget!=0:
		print("Connection to: \"" + host + ":" + str(port) + " " + selector + "\" Terminated early.")
	gsocket.close()
	tmpbuff.seek(0)
	print("done.")
	return tmpbuff


if __name__=="__main__":
	gdat=gopherget("gopher.floodgap.com", 70, "")
	menulist=menudecode(gdat)
	for item in menulist:
		print(item.name)