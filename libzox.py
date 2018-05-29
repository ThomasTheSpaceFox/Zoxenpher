#!/usr/bin/env python
#import time
import os
import libgop
import pygame
from threading import Thread
#import copy
#import sys

#determines if a host-port-selector location is one of zoxenpher's special "about:" paths or a normal gopher location.
#also brings up appropiate error pages and images in the event of load failures.
def pathfigure(host, port, selector, gtype="0"):
	if host.startswith("about:"):
		hoststripped=host.replace('\\', "").replace("/", "").replace("..", "")
		hoststripped=hoststripped[6:]
		if os.path.isfile(os.path.join("vgop", hoststripped)):
			data=open(os.path.join("vgop", hoststripped))
		else:
			if gtype=="1":
				data=open(os.path.join("vgop", "gaierror"))
			if gtype=="0":
				data=open(os.path.join("vgop", "gaierror.txt"))
			if gtype=="p":
				data=open(os.path.join("vgop", "gaierror.png"))
			if gtype=="I" or gtype=="g":
				data=open(os.path.join("vgop", "gaierror.gif"))
	else:
		try:
			data=libgop.gopherget(host, port, selector)
		except Exception as err:
			print(err)
			if gtype=="1":
				data=open(os.path.join("vgop", "gaierror"))
			if gtype=="0":
				data=open(os.path.join("vgop", "gaierror.txt"))
			if gtype=="p":
				data=open(os.path.join("vgop", "gaierror.png"))
			if gtype=="I" or gtype=="g":
				data=open(os.path.join("vgop", "gaierror.gif"))
	return data


#displays text and links with automatic word wrap.
def textitem(text, xfont, yjump, textcolx, surface, ypos, renderdict, itemicn=None, link=0, xoff=26):
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
					dictkey=str(textcolx[0])+str(textcolx[1])+str(textcolx[2])+buffstring
					if dictkey in renderdict:
						namelabel=renderdict[dictkey]
					else:
						if link:
							namelabel=xfont.render(buffstring.strip(), True, textcolx, (255, 255, 255))
						else:
							namelabel=xfont.render(buffstring, True, textcolx, (255, 255, 255))
						renderdict[dictkey]=namelabel
					rectlist.extend([surface.blit(namelabel, (xpos, ypos))])
					
				ypos+=yjump
			elif xfont.size(buffstring+word+" ")[0]<=(surface.get_width()-xoff):
				buffstring+=word+" "
			else:
				if ypos>=(-30-yjump) and ypos<=surface.get_height():
					dictkey=str(textcolx[0])+str(textcolx[1])+str(textcolx[2])+buffstring
					if dictkey in renderdict:
						namelabel=renderdict[dictkey]
					else:
						if link:
							namelabel=xfont.render(buffstring.strip(), True, textcolx, (255, 255, 255))
						else:
							namelabel=xfont.render(buffstring, True, textcolx, (255, 255, 255))
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
def imgget(items, uptref, frameobj):
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
			mitem.image=imagefx
		except pygame.error:
			return
	if uptref!=None:
		uptref(frameobj)

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


cnfdef={"imgpreview" : "10",
"histsize" : "10",
"deskw" : "800",
"deskh" : "600",
"menufontsize" : "15",
"menutextjump" : "15",
"menufont" : "mono",
"menuheight" : "460",
"bgtile" : "diagbg.png"}






def cnfload():
	cnfdict=cnfdef.copy()
	try:
		cnffile=open(os.path.join("usr", "cnf.dat"))
		for line in cnffile:
			if not line.startswith("#") and "=" in line:
				line=line.replace("\n", "").replace("\r", "")
				item, data = line.split("=")
				if item in cnfdict:
					cnfdict[item]=data
	except IOError:
		return cnfdict
	return cnfdict
print("Libzox: loading configuration data.")
cnfdict=cnfload()

#draw tiles (tilesurf) on a copy of a surface (drawsurf)
def tiledraw(drawsurf, tilesurf):
	drawsurf=drawsurf.copy()
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

