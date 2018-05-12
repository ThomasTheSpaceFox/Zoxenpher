#!/usr/bin/env python
import time
import os
import libgop
import pygame
from threading import Thread
import copy
import sys

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
def textitem(text, xfont, yjump, textcolx, surface, ypos, renderdict):
	xpos=0
	rectlist=[]
	words=text.split(" ")
	if True:
		buffstring=""
		for word in words+[" ", None]:
			
			#print buffstring
			if word==None:
				dictkey=str(textcolx[0])+str(textcolx[1])+str(textcolx[2])+buffstring
				if dictkey in renderdict:
					namelabel=renderdict[dictkey]
				else:
					namelabel=xfont.render(buffstring, True, textcolx, (255, 255, 255))
					renderdict[dictkey]=namelabel
				rectlist.extend([surface.blit(namelabel, (xpos, ypos))])
				ypos+=yjump
			elif xfont.size(buffstring+word+" ")[0]<=surface.get_width():
				buffstring+=word+" "
			else:
				dictkey=str(textcolx[0])+str(textcolx[1])+str(textcolx[2])+buffstring
				if dictkey in renderdict:
					namelabel=renderdict[dictkey]
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
	def __init__(self, classref, icon, idcode, friendly_name, commname, xsize, ysize, resizable=0, key=None, mod=None, hint=""):
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

#special gopherpane "launch icon" class. used by help icon to bring up "about:help"
class pathprogobj:
	def __init__(self, classref, icon, idcode, friendly_name, commname, xsize, ysize, resizable=0, key=None, mod=None, host="about:splash", port=70, selector="/", hint=""):
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