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

#determines if a host-port-selector location is one of zoxenpher's special "about:" paths or a normal gopher location.
#also brings up appropiate error pages and images in the event of load failures.
def pathfigure(host, port, selector, gtype="0"):
	data=None
	if host.startswith("about:"):
		hoststripped=host.replace('\\', "").replace("/", "").replace("..", "")
		hoststripped=hoststripped[6:]
		if os.path.isfile(os.path.join("vgop", hoststripped)):
			data=open(os.path.join("vgop", hoststripped))
		elif os.path.isfile(os.path.join("vgop", hoststripped+".gop")):
			data=open(os.path.join("vgop", hoststripped+".gop"))
		else:
			if gtype=="1":
				data=open(os.path.join("vgop", "E_localerror"))
			if gtype=="0":
				data=open(os.path.join("vgop", "E_localerror.txt"))
			if gtype=="p":
				data=open(os.path.join("vgop", "gaierror.png"))
			if gtype=="I" or gtype=="g":
				data=open(os.path.join("vgop", "gaierror.gif"))
	else:
		try:
			data=libgop.gopherget(host, port, selector)
		except socket.timeout as err:
			print(err)
			if gtype=="1":
				data=open(os.path.join("vgop", "E_timeout"))
			if gtype=="0":
				data=open(os.path.join("vgop", "E_timeout.txt"))
			if gtype=="p":
				data=open(os.path.join("vgop", "gaierror.png"))
			if gtype=="I" or gtype=="g":
				data=open(os.path.join("vgop", "gaierror.gif"))
		except socket.error as err:
			print(err)
			if gtype=="1":
				data=open(os.path.join("vgop", "E_serror"))
			if gtype=="0":
				data=open(os.path.join("vgop", "E_serror.txt"))
			if gtype=="p":
				data=open(os.path.join("vgop", "gaierror.png"))
			if gtype=="I" or gtype=="g":
				data=open(os.path.join("vgop", "gaierror.gif"))
		except socket.gaierror as err:
			print(err)
			if gtype=="1":
				data=open(os.path.join("vgop", "E_gaierror"))
			if gtype=="0":
				data=open(os.path.join("vgop", "E_gaierror.txt"))
			if gtype=="p":
				data=open(os.path.join("vgop", "gaierror.png"))
			if gtype=="I" or gtype=="g":
				data=open(os.path.join("vgop", "gaierror.gif"))
		except socket.herror as err:
			print(err)
			if gtype=="1":
				data=open(os.path.join("vgop", "E_herror"))
			if gtype=="0":
				data=open(os.path.join("vgop", "E_herror.txt"))
			if gtype=="p":
				data=open(os.path.join("vgop", "gaierror.png"))
			if gtype=="I" or gtype=="g":
				data=open(os.path.join("vgop", "gaierror.gif"))
		except Exception as err:
			print(err)
			if gtype=="1":
				data=open(os.path.join("vgop", "E_undeferror"))
			if gtype=="0":
				data=open(os.path.join("vgop", "E_undeferror.txt"))
			if gtype=="p":
				data=open(os.path.join("vgop", "gaierror.png"))
			if gtype=="I" or gtype=="g":
				data=open(os.path.join("vgop", "gaierror.gif"))
	return data

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
def textitem(text, xfont, yjump, textcolx, surface, ypos, renderdict, itemicn=None, link=0, xoff=26, textcoly=(255, 255, 255)):
	xpos=0
	rectlist=[]
	words=text.split(" ")
	if itemicn!=None and ypos>=(-30-yjump) and ypos<=surface.get_height():
		
		rectlist.extend([surface.blit(itemicn, (xpos, ypos))])
		if 25>yjump:
			yjump=25
	xpos=xoff
	
	if True:
		buffstring=""
		for word in words+[" ", None]:
			
			#print buffstring
			if word==None:
				if ypos>=(-30-yjump) and ypos<=surface.get_height():
					dictkey=str(textcolx[0])+"\t"+str(textcolx[1])+"\t"+str(textcolx[2])+"\t"+buffstring
					if dictkey in renderdict:
						namelabel=renderdict[dictkey]
					else:
						if link:
							namelabel=xfont.render(buffstring.strip(), True, textcolx, textcoly)
						else:
							namelabel=xfont.render(buffstring, True, textcolx, textcoly)
						renderdict[dictkey]=namelabel
					rectlist.extend([surface.blit(namelabel, (xpos, ypos))])
					
				ypos+=yjump
			elif xfont.size(buffstring+word+" ")[0]<=(surface.get_width()-xoff):
				buffstring+=word+" "
			else:
				if ypos>=(-30-yjump) and ypos<=surface.get_height():
					dictkey=str(textcolx[0])+"\t"+str(textcolx[1])+"\t"+str(textcolx[2])+"\t"+buffstring
					if dictkey in renderdict:
						namelabel=renderdict[dictkey]
					else:
						if link:
							namelabel=xfont.render(buffstring.strip(), True, textcolx, textcoly)
						else:
							namelabel=xfont.render(buffstring, True, textcolx, textcoly)
						renderdict[dictkey]=namelabel
					rectlist.extend([surface.blit(namelabel, (xpos, ypos))])
				
				ypos+=yjump
				buffstring=word+" "
	if len(rectlist)>0:
		return (rectlist[0].unionall(rectlist), ypos, renderdict)
	else:
		return (pygame.Rect(0, 0, 0, 0), ypos, renderdict)


#normal "launch icon" class
class progobj:
	def __init__(self, classref, icon, idcode, friendly_name, commname, xsize, ysize, resizable=0, key=None, mod=None, hint="", side=0):
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

#special gopherpane "launch icon" class. used by help icon to bring up "about:help"
class pathprogobj:
	def __init__(self, classref, icon, idcode, friendly_name, commname, xsize, ysize, resizable=0, key=None, mod=None, host="about:splash", port=70, selector="/", hint="", side=0):
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
	def classref(self):
		return self.classrefx(host=self.host, port=self.port, selector=self.selector)

#image loader routine. (runs in separate thread when needed)
def imgget(items, uptref, frameobj, gopherwindow):
	for mitem in items:
		data=pathfigure(mitem.hostname, mitem.port, mitem.selector, gtype=mitem.gtype)
		try:
			if mitem.gtype=="g":
				imagefx=pygame.image.load(data, "quack.gif")
			if mitem.gtype=="p":
				imagefx=pygame.image.load(data, "quack.png")
			if mitem.gtype=="I":
				imagefx=pygame.image.load(data)
			imagefx.convert()
			mitem.fullimage=imagefx
			mitem.image=imagelimit_gwindow(imagefx, frameobj.surface.get_width()-30, 1800)
		except pygame.error:
			gopherwindow.loading=0
			return
	gopherwindow.loading=0
	if uptref!=None:
		uptref(frameobj)
	

def reshrinkimages(items, frameobj):
	for mitem in items:
		if mitem.image!=None:
			mitem.image=imagelimit_gwindow(mitem.fullimage, frameobj.surface.get_width()-30, 1800)


def gurlencode(host, selector, gtype, port=70):
	if int(port)==70:
		return (host + "/" + gtype + selector)
	else:
		return (host + "/" + gtype + selector + ":" + str(port))

def gurldecode(url):
	if url.startswith("gopher://"):
		url.replace("gopher://", "")
	stringblob=url
	if stringblob.startswith("about:"):
		host=stringblob
		port=70
		selector=""
		#self.gtype="1"
		if "/" in stringblob:
			host, selecttype = stringblob.split("/", 1)
			gtype=selecttype[0]
		else:
			gtype="1"
	else:
		
		if ":" in stringblob:
			port=stringblob.split(":")[1]
			stringblob=stringblob.split(":")[0]
		else:
			port=70
		if "/" in stringblob:
			host, selecttype = stringblob.split("/", 1)
			gtype=selecttype[0]
			selector=selecttype[1:]
		else:
			host=stringblob
			gtype="1"
			selector="/"
	return host, port, selector, gtype


class histitem:
	def __init__(self, host, port, selector, gtype, data, menu):
		self.host=host
		self.selector=selector
		self.port=port
		self.data=data
		self.menu=menu
		self.gtype=gtype

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
cnfbools=["itemdebug"]
cnfints=["imgpreview", "bgmode", "histsize", "deskw", "deskh", "menufontsize", "menutextjump", "menuheight", "framestyle", "wmfps", "viewzoom"]

cnfdef={"imgpreview" : "10",
"histsize" : "10",
"deskw" : "800",
"deskh" : "600",
"menufontsize" : "15",
"menutextjump" : "15",
"menufont" : "mono",
"menuheight" : "460",
"bgtile" : "diagbg.png",
"framestyle" : "2",
"wmfps" : "30",
"itemdebug" : "0",
"viewzoom" : "2400",
"browser" : "none",
"bgmode" : "1"}

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
def tiledraw(drawsurf, tilesurf):
	bgmode=int(cnfdict["bgmode"])
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
		return drawsurf
	if bgmode==0:
		xpos=drawsurf.get_width()//2-tilesurf.get_width()//2
		ypos=drawsurf.get_height()//2-tilesurf.get_height()//2
		drawsurf.blit(tilesurf, (xpos, ypos))
		return drawsurf
	else:
		destwidth=drawsurf.get_width()
		destheight=drawsurf.get_height()
		pygame.transform.scale(tilesurf, (destwidth, destheight), drawsurf)
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

