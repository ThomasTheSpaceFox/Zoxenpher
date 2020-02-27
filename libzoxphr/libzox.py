#!/usr/bin/env python
#import time
import os
import sys
from . import libgop
import pygame
from threading import Thread
import socket
#import copy
#import sys

gfxpath=os.path.join("vgop", "gfx")
internalurlhosts=["zox>>", "zoxhelp>>", "zoxsplash>>", "file>>"]

def isinternalurl(url):
	for host in internalurlhosts:
		if url.startswith(host):
			return 1
	return 0
def isinternalhost(host):
	if host in internalurlhosts:
		return 1
	return 0



#determines if a host-port-selector location is one of zoxenpher's special "about:" paths or a normal gopher location.
#also brings up appropiate error pages and images in the event of load failures.
errorpath=os.path.join("vgop", "error")
def pathfigure(host, port, selector, gtype="0", query=None):
	data=None
	#legacy internal doc URL scheme (DO NOT USE!!!!)
	#if host.startswith("about:"):
		#print("Legacy WARNING: old 'about:' internal URL accessed!\n\t'"+host+"'")
		#hoststripped=host.replace('\\', "").replace("/", "").replace("..", "")
		#hoststripped=hoststripped[6:]
		#if os.path.isfile(os.path.join("vgop", hoststripped)):
			#data=open(os.path.join("vgop", hoststripped))
		#elif os.path.isfile(os.path.join("vgop", hoststripped+".gop")):
			#data=open(os.path.join("vgop", hoststripped+".gop"))
		#else:
			#if gtype=="1":
				#data=open(os.path.join(errorpath, "E_localerror"))
			#if gtype=="0":
				#data=open(os.path.join(errorpath, "E_localerror.txt"))
			#if gtype=="p":
				#data=open(os.path.join(errorpath, "gaierror.png"))
			#if gtype=="I" or gtype=="g":
				#data=open(os.path.join(errorpath, "gaierror.gif"))
	#new internal doc URL scheme.
	#these "fake" hosts, enact hardcoded file loading/internal page generation activity.
	if host==("zox>>") or host=="zoxhelp>>" or host=="zoxsplash>>" or host=="file>>":
		#run special fileurl listing code. if not a directory, normal internal doc code runs.
		if host=="file>>" and gtype=="1":
			fileurldata=fileurl(host, port, selector)
			if fileurldata!=None:
				return fileurldata
		#hoststripped=host.replace('\\', "").replace("/", "").replace("..", "")
		#hoststripped=hoststripped[6:]
		selectorlist=selector.split("/")
		
		if "" in selectorlist:
			selectorlist.remove("")
		if "." in selectorlist:
			selectorlist.remove(".")
		if ".." in selectorlist:
			selectorlist.remove("..")
		#add help prefix path for zoxhelp>> URLs
		if host=="zoxhelp>>":
			selectorlist=["vgop", "help"]+selectorlist
		if host=="zoxsplash>>":
			selectorlist=["vgop", "splash"]+selectorlist
		selectorlist=["."]+selectorlist
		selectpath=os.path.join(*selectorlist)
		#selectdir=os.path.join(*selectorlist)
		if os.path.isfile(selectpath):
			data=open(selectpath)
		elif os.path.isfile(selectpath+".gop"):
			data=open(selectpath+".gop")
		elif os.path.isfile(os.path.join(selectpath, "index.gop")):
			data=open(os.path.join(selectpath, "index.gop"))
		else:
			data=PathErrorHandle(selector, host, port, "Internal URL Error! [error s3]", "Zoxenpher was unable to load that inernal URL.", gtype=gtype, querytext=query)
	else:
		try:
			data=libgop.gopherget(host, port, selector, query)
		except socket.timeout as err:
			print(err)
			data=PathErrorHandle(selector, host, port, "Connection timeout. (socket.timeout) [error s1]", "The connection timed out.", errraw=err, gtype=gtype, querytext=query)
		except socket.error as err:
			print(err)
			data=PathErrorHandle(selector, host, port, "Generic Socket Error (socket.error) [error s5]", "Zoxenpher was unable to load that gopher address!", errraw=err, gtype=gtype, querytext=query)
		except socket.gaierror as err:
			print(err)
			data=PathErrorHandle(selector, host, port, "Socket Error (socket.gaierror) [error s0]", "Zoxenpher was unable to load that gopher address!", errraw=err, gtype=gtype, querytext=query)
		except socket.herror as err:
			print(err)
			data=PathErrorHandle(selector, host, port, "Socket Error (socket.herror) [error s4]", "Zoxenpher was unable to load that gopher address!", errraw=err, gtype=gtype, querytext=query)
		except Exception as err:
			print(err)
			data=PathErrorHandle(selector, host, port, "Unknown Error [error s2]"  , "An unknown error occured when trying to make a connection.", errraw=err, gtype=gtype, querytext=query)
	return data

default_heading_divider="_________________________________________________________________"

#Filters external gopher menus for any possible security issues, i.e. trying to refrence internal zoxenpher URLs
def SecureFilter(menulist, serverhost):
	#if its an internal URL, the anti-internal url filter (obviously) should not run.
	if isinternalhost(serverhost):
		return menulist
	else:
		for item in menulist:
			#block external gopher menus referencing internal Zoxenpher urls.
			if item.gtype!="i" and isinternalhost(item.hostname):
				#errorstring="WARNING: internal URL selector on external menu! Debug: " + item.debug
				#item.debug=errorstring
				#item.name=errorstring
				
				item.errortype=libgop.ERR_SECURITY
				item.errorlabel="MENU SECURITY FILTER"
				item.errorinfo="An Internal URL was detected in a selector on an external server's menu. For security reasons, Zoxenpher blocks external refrences to internal URLs, showing instead an error message."
				item.gtype=None
				item.hostname=None
				item.selector=None
				item.datalist=None
		return menulist

def ientry(string, gtype="i", selector="null", host="null"):
	return gtype+string+"\t"+selector+"\t"+host+"\t70"

def PathErrorHandle(selector, host, port, errorstr, errordesc, errraw=None, gtype="1", querytext=None):
	#print(gtype)
	if errraw!=None:
		errraw=str(errraw)
	if isinternalhost(host):
		iurl="Yes"
	else:
		iurl="No"
	if gtype=="7" or gtype=="1":
		data=[]
		if not isinternalhost(host):
			data.append(ientry("Network Error:"))
		else:
			data.append(ientry("Internal Error:"))
		data.append(ientry(errorstr, gtype="3"))
		data.append(ientry(default_heading_divider))
		data.append(ientry(errordesc))
		#triggers security filter on external urls.
		#data.append(ientry("", gtype="p", selector="/vgop/error/generic.png", host="zox>>"))
		data.append(ientry("Host: " + str(host)))
		data.append(ientry("Port: " + str(port)))
		data.append(ientry("Selector: " + str(selector)))
		if querytext!=None:
			data.append(ientry("Query: " + str(querytext)))
		data.append(ientry("Gopher Type: " + str(gtype)))
		data.append(ientry("Internal Url: " + iurl))
		
		data.append(ientry(default_heading_divider))
		if errraw!=None:
			data.append(ientry("--Error Details--"))
			data.append(ientry("'" + errraw.replace("\t", "   ").replace("\n", "") + "'"))
			data.append(ientry(default_heading_divider))
		data.append(ientry("This page was generated internally by Zoxenpher."))
		data.append(".")
		return data
	if gtype=="0":
		data=[]
		if not isinternalhost(host):
			data.append(("Network Error:"))
		else:
			data.append(("Internal Error:"))
		data.append((errorstr))
		data.append((default_heading_divider))
		data.append((errordesc))
		data.append(("Host: " + str(host)))
		data.append(("Port: " + str(port)))
		data.append(("Selector: " + str(selector)))
		data.append(("Gopher Type: " + str(gtype)))
		data.append(("Internal Url: " + iurl))
		data.append((default_heading_divider))
		if errraw!=None:
			data.append(("--Error Details--"))
			data.append(("'" + errraw.replace("\t", "   ").replace("\n", "") + "'"))
			data.append((default_heading_divider))
		data.append(("This page was generated internally by Zoxenpher."))
		return data
	if gtype=="p":
		return open(os.path.join(errorpath, "gaierror.png"))
	if gtype=="I" or gtype=="g":
		return open(os.path.join(errorpath, "gaierror.gif"))
	return None

def fileurl_pathlist(host, port, selector, selectorlist):
	ext=None
	gtype=None
	data=[ientry("-- Directory Listing: '"+selector+"' --")]
	data.append(ientry(default_heading_divider))
	realpath=os.path.join(*selectorlist)
	for filen in os.listdir(realpath):
		if selector=="" or selector=="/":
			filepath="/"+filen
		else:
			filepath=selector+"/"+filen
		realfilepath=os.path.join(realpath, filen)
		if filen.startswith("."):
			pass
		elif os.path.isfile(realfilepath):
			if "." in filen:
				ext=filen.lower().rsplit(".")[-1]
			else:
				ext=None
			if ext=="png":
				gtype="p"
			elif ext=="gif":
				gtype="g"
			elif ext=="gop":
				gtype="1"
			
			elif ext in ["jpg", "jpeg", "bmp"]:
				gtype="I"
			elif ext in ["txt", "md", "cfg", "dat"]:
				gtype="0"
			elif ext in ["wav", "mp3", "mod", "ogg", "oga", "midi", "mid"]:
				gtype="s"
			else:
				ext=None
				gtype=None
			if ext!=None and gtype!=None:
				data.append(ientry("---- "+filen))
				data.append(ientry("Open", gtype=gtype, host="file>>", selector=filepath))
				#data.append(ientry("Info", gtype="1", host="fileinfo>>", selector=filepath))
				data.append(ientry(""))
		elif os.path.isdir(realfilepath):
			data.append(ientry("DIR- "+filen))
			data.append(ientry("Open", gtype="1", host="file>>", selector=filepath))
			data.append(ientry(""))
	data.append(ientry(default_heading_divider))
	data.append(ientry("This page was generated internally by Zoxenpher."))
	return data
	

def fileurl(host, port, selector):
	selectorlist=selector.split("/")
	if "" in selectorlist:
		selectorlist.remove("")
	if "." in selectorlist:
		selectorlist.remove(".")
	if ".." in selectorlist:
		selectorlist.remove("..")
	selectorlist=["."]+selectorlist
	selectpath=os.path.join(*selectorlist)
	#data=[ientry("The path: '"+selector+"' is not a directory.", gtype="3")]
	if os.path.isdir(selectpath):
		return fileurl_pathlist(host, port, selector, selectorlist)
	return None
			
	

#ratio-preserving image shrinker
def imagelimit(surf, maxsize):

	if surf.get_width()>maxsize or surf.get_height()>maxsize:
		xsize=surf.get_width()
		ysize=surf.get_height()
		
		yscale=float(maxsize)/ysize
		xscale=float(maxsize)/xsize
		if xscale<yscale:
			scale=xscale
		else:
			scale=yscale
			
		return pygame.transform.scale(surf, (int(xsize*scale), int(ysize*scale)))
	return surf
	


def imagelimit_gwindow(surf, maxsize, heightmax):

	if surf.get_width()>maxsize or surf.get_height()>maxsize:
		xsize=surf.get_width()
		ysize=surf.get_height()
		
		scale=float(maxsize)/xsize
			
		return imagelimit(pygame.transform.scale(surf, (int(xsize*scale), int(ysize*scale))), heightmax)
	return imagelimit(surf, heightmax)




#displays text and links with automatic word wrap.
def textitem(text, xfont, yjump, textcolx, surface, ypos, renderdict, itemicn=None, link=0, xoff=26, textcoly=(255, 255, 255), iconsize=25, roff=0):
	xpos=0
	yposstart=ypos
	#####don't bother with items beyond the end of the screen, as theres no point.
	#YES BOTHER WITH THEM!
	#if ypos>surface.get_height():
	#	return (pygame.Rect(0, 0, 0, 0), ypos, renderdict)
	#upper position of rendering
	top_offset=-30-yjump
	#generate renderdict key for storing height, use to read cached
	#   height and return quickly (if height cached)
	#NOTE: its OK if the same line of text is duplicated, as it will
	#   word-wrap the exact same way, and hence, be the same height.
	sizekey="YSIZECACHE-" + text + "---"
	if ypos<=top_offset or ypos>=surface.get_height():
		if sizekey in renderdict:
			return (pygame.Rect(0, 0, 0, 0), renderdict[sizekey]+ypos, renderdict)
	
	
	rectlist=[]
	words=text.split(" ")
	
	if itemicn!=None and ypos>=top_offset:
		
		rectlist.extend([surface.blit(itemicn, (xpos, ypos))])
		if iconsize>yjump:
			yjump=iconsize
	xpos=xoff
	
	if True:
		buffstring=""
		for word in words+[" ", None]:
			
			#print buffstring
			if word==None:
				if ypos>=top_offset and ypos<=surface.get_height():
					dictkey=str(textcoly[0])+"\t"+str(textcoly[1])+"\t"+str(textcoly[2])+"\t"+str(textcolx[0])+"\t"+str(textcolx[1])+"\t"+str(textcolx[2])+"\t"+buffstring
					if dictkey in renderdict:
						namelabel=renderdict[dictkey]
					else:
						if link:
							namelabel=xfont.render(buffstring.strip(), True, textcolx, textcoly)
						else:
							namelabel=xfont.render(buffstring.rstrip(), True, textcolx, textcoly)
						renderdict[dictkey]=namelabel
					rectlist.extend([surface.blit(namelabel, (xpos, ypos))])
					
				ypos+=yjump
			elif xfont.size(buffstring+word+" ")[0]<=(surface.get_width()-xoff-roff):
				buffstring+=word+" "
			else:
				if ypos>=top_offset and ypos<=surface.get_height():
					dictkey=str(textcoly[0])+"\t"+str(textcoly[1])+"\t"+str(textcoly[2])+"\t"+str(textcolx[0])+"\t"+str(textcolx[1])+"\t"+str(textcolx[2])+"\t"+buffstring
					if dictkey in renderdict:
						namelabel=renderdict[dictkey]
					else:
						if link:
							namelabel=xfont.render(buffstring.strip(), True, textcolx, textcoly)
						else:
							namelabel=xfont.render(buffstring.rstrip(), True, textcolx, textcoly)
						renderdict[dictkey]=namelabel
					rectlist.extend([surface.blit(namelabel, (xpos, ypos))])
				
				ypos+=yjump
				buffstring=word+" "
		#store size in renderdict using sizekey, if its not already present.
		if sizekey not in renderdict:
			renderdict[sizekey]=ypos-yposstart
	if len(rectlist)>0:
		return (rectlist[0].unionall(rectlist), ypos, renderdict)
	else:
		return (pygame.Rect(0, 0, 0, 0), ypos, renderdict)


#normal "launch icon" class
class progobj:
	def __init__(self, classref, icon, idcode, friendly_name, commname, xsize, ysize, resizable=0, key=None, mod=None, hint="", side=0, ghost=0):
		self.idcode=idcode
		self.friendly_name=friendly_name
		self.commname=commname
		self.icon=icon
		self.xsize=xsize
		self.ysize=ysize
		self.classref=classref
		self.resizable=resizable
		self.key=key
		self.mod=mod
		self.hint=hint
		self.side=side
		self.ghost=ghost

#special gopherpane "launch icon" class. used by help icon to bring up help index.
class pathprogobj:
	def __init__(self, classref, icon, idcode, friendly_name, commname, xsize, ysize, resizable=0, key=None, mod=None, host="zoxsplash>>", port=70, selector="/", hint="", side=0):
		self.idcode=idcode
		self.friendly_name=friendly_name
		self.commname=commname
		self.icon=icon
		self.xsize=xsize
		self.ysize=ysize
		self.classrefx=classref
		self.resizable=resizable
		self.key=key
		self.mod=mod
		self.host=host
		self.port=port
		self.selector=selector
		self.hint=hint
		self.side=side
		self.ghost=0
	def classref(self):
		return self.classrefx(host=self.host, port=self.port, selector=self.selector)

#image loader routine. (runs in separate thread when needed)
#MOVED TO INSIDE GOPHERPANE
#def imgget(items, uptref, frameobj, gopherwindow):
	#for mitem in items:
		##stop loading if menu window is closed.
		#if frameobj.runflg==0:
			#return
		#data=pathfigure(mitem.hostname, mitem.port, mitem.selector, gtype=mitem.gtype)
		#try:
			#if mitem.gtype=="g":
				#imagefx=pygame.image.load(data, "quack.gif")
			#if mitem.gtype=="p":
				#imagefx=pygame.image.load(data, "quack.png")
			#if mitem.gtype=="I":
				#imagefx=pygame.image.load(data)
			#imagefx.convert()
			#mitem.fullimage=imagefx
			#mitem.image=imagelimit_gwindow(imagefx, frameobj.surface.get_width()-30, 1800)
		#except pygame.error:
			#gopherwindow.loading=0
			#return
	#gopherwindow.loading=0
	#if uptref!=None:
		#uptref(frameobj)
	

def reshrinkimages(items, frameobj):
	for mitem in items:
		if mitem.image!=None:
			mitem.image=imagelimit_gwindow(mitem.fullimage, frameobj.surface.get_width()-30, 1800)


def gurlencode(host, selector, gtype, port=70, query=None):
	if query==None:
		qtext=""
	else:
		qtext="?"+query
	if int(port)==70:
		return (host + "/" + gtype + selector + qtext)
	else:
		return (host + ":" + str(port) + "/" + gtype + selector + qtext)

def gurldecode(url):
	if url.startswith("gopher://"):
		url.replace("gopher://", "")
	stringblob=url
	if stringblob.startswith("about:"):
		host=stringblob
		port=70
		selector=""
		query=None
		#self.gtype="1"
		if "/" in stringblob:
			host, selecttype = stringblob.split("/", 1)
			gtype=selecttype[0]
		else:
			gtype="1"
	else:
		if "?" in stringblob:
			query=stringblob.split("?")[1]
			stringblob=stringblob.split("?")[0]
		else:
			query=None
		
		if "/" in stringblob:
			host, selecttype = stringblob.split("/", 1)
			gtype=selecttype[0]
			selector=selecttype[1:]
		else:
			host=stringblob
			gtype="1"
			selector="/"
		if ":" in host:
			port=host.split(":")[1]
			host=host.split(":")[0]
		else:
			port=70
	return host, port, selector, gtype, query


class histitem:
	def __init__(self, host, port, selector, gtype, data, menu, query):
		self.host=host
		self.selector=selector
		self.port=port
		self.data=data
		self.menu=menu
		self.gtype=gtype
		self.query=query

class bmitem:
	def __init__(self, url, name):
		self.url=url
		self.name=name
		self.rect=None


def bmload():
	bmlist=[]
	bmfilename=os.path.join("usr", "bm.dat")
	try:
		bmfile=open(bmfilename, 'r')
		for line in bmfile:
			line=line.replace("\n", "").replace("\r", "")
			url, name = line.split("\t")
			bmlist.extend([bmitem(url, name)])
		bmfile.close()
		return bmlist
	except IOError:
		return []
		

def bmsave(bmlist):
	bmfilename=os.path.join("usr", "bm.dat")
	bmfile=open(bmfilename, 'w')
	for item in bmlist:
		bmfile.write(item.url + "\t" + item.name + "\n")
	bmfile.close()

#bmlist=bmload()
#bmlist.extend([bmitem("about:splash", "Splash page")])
#bmsave(bmlist)

#syntax check lists
cnfbools=["itemdebug", "showzoxban", "imgprevbool"]
cnfints=["imgpreview", "bgmode", "histsize", "deskw", "deskh", "menufontsize", "menutextjump", "menuheight", "framestyle", "wmfps", "viewzoom"]

cnfdef={"imgpreview" : "10",
"histsize" : "10",
"deskw" : "800",
"deskh" : "600",
"menufontsize" : "15",
"menutextjump" : "15",
"menufont" : "mono",
"menuheight" : "460",
"bgtile" : "zoxnewbg.png",
"framestyle" : "1",
"wmfps" : "30",
"itemdebug" : "0",
"viewzoom" : "2400",
"browser" : "none",
"telnet" : "none",
"telnet3270" : "none",
"bgmode" : "1",
"showzoxban" : "1",
"imgprevbool" : "1"}

itemdebug=0


def cnfbool(cvalue):
	if cvalue.lower() in ["1", "true", "on", "yes"]:
		return 1
	else:
		return 0
def cnfint(cvalue):
	try:
		return int(cvalue)
	except ValueError:
		return None
def cnfload():
	global itemdebug
	cnfdict=cnfdef.copy()
	try:
		cnffile=open(os.path.join("usr", "cnf.dat"))
		for line in cnffile:
			if not line.startswith("#") and "=" in line:
				line=line.replace("\n", "").replace("\r", "")
				item, data = line.split("=")
				if item in cnfdict:
					
					if item in cnfbools:
						cnfdict[item]=cnfbool(data)
					elif item in cnfints:
						retval=cnfint(data)
						if retval==None:
							sys.exit("ERROR: invalid syntax in configuration file. config setting: '" + item + "' requires an integer.")
						cnfdict[item]=retval
					else:
						cnfdict[item]=data
						
	except IOError:
		return cnfdict
	#set debug option vars.
	itemdebug=int(cnfdict["itemdebug"])
	return cnfdict
print("Libzox: loading configuration data.")
cnfdict=cnfload()

#draw tiles (tilesurf) on a copy of a surface (drawsurf)
def tiledraw(drawsurf, tilesurf, zban):
	bgmode=int(cnfdict["bgmode"])
	zbanflag=int(cnfdict["showzoxban"])
	drawsurf=drawsurf.copy()
	if bgmode==1:
		destwidth=drawsurf.get_width()
		destheight=drawsurf.get_height()
		sourcewidth=tilesurf.get_width()
		sourceheight=tilesurf.get_height()
		ywid=0
		while ywid<=destheight:
			xwid=0
			while xwid<=destwidth:
				drawsurf.blit(tilesurf, (xwid, ywid))
				xwid+=sourcewidth
			ywid+=sourceheight
		#return drawsurf
	elif bgmode==0:
		xpos=drawsurf.get_width()//2-tilesurf.get_width()//2
		ypos=drawsurf.get_height()//2-tilesurf.get_height()//2
		drawsurf.blit(tilesurf, (xpos, ypos))
		#return drawsurf
	else:
		destwidth=drawsurf.get_width()
		destheight=drawsurf.get_height()
		pygame.transform.scale(tilesurf, (destwidth, destheight), drawsurf)
	if zbanflag:
		xpos=drawsurf.get_width()//2-zban.get_width()//2
		ypos=drawsurf.get_height()//2-zban.get_height()//2
		drawsurf.blit(zban, (xpos, ypos))
	return drawsurf

### timer for pumpcalls
class tickdo:
	def __init__(self, ticks):
		self.tickend=ticks
		self.ticks=0
	def tick(self):
		self.ticks+=1
		if self.tickend==self.ticks:
			self.ticks=0
			return 1
		else:
			return 0

