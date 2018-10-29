#!/usr/bin/env python
import os
import pygame
import time
import math
pygame.display.init()
pygame.font.init()
#ui styling globals
framepad=8
hudsize=20
fontsize=25

resizebar=10
#0=plain, 1=3D, 2=3D2
framestyle=2
#window manager speed in fps.
wmfps=30

#lower ypos limit (for toolbars/taskbars/etc on top of main window.)
#offset constants for each frame style.
minyoffset0=25
minyoffset1=27
minyoffset2=31
#helpful offset setting for desktop taskbars/toolbars on top of main window.
miny=0


def setminy(newminy):
	global miny
	
	if framestyle==0:
		miny=newminy+minyoffset0-1
		return
	elif framestyle==1:
		miny=newminy+minyoffset1-1
		return
	elif framestyle==2:
		miny=newminy+minyoffset2-1
		return
		
setminy(0)

titlecache={}
titlecacheact={}
#maximum size of titlecache and titlecacheact before clearing them.
titlecachelimit=40

def cachesizecheck():
	global titlecache
	global titlecacheact
	if len(titlecache)>titlecachelimit:
		del titlecache
		titlecache={}
		#print("StrazoloidWM: clear title cache inact")
	if len(titlecacheact)>titlecachelimit:
		del titlecacheact
		titlecacheact={}
		#print("StrazoloidWM: clear title cache act")


def mousehelper(mpos, frameobj):
	return (mpos[0]-frameobj.xpos, mpos[1]-frameobj.ypos)

def getframe_shadeaware(frame, surfrect, resize=0):
	if framestyle!=2:
		framerect=surfrect.inflate(framepad, framepad)
		
	else:
		framerect=surfrect.inflate(1, 1)
		framerect.y-=framepad//2+4
		framerect.h+=framepad//2+4
		framerect.x-=2
		framerect.w+=1
	framerect.y-=hudsize
	framerect.h+=hudsize
	if frame.shade:
		framerect.h-=surfrect.h
		if framestyle==2:
			framerect.h-=5
	elif resize:
		framerect.h+=resizebar
	if framestyle==1:
		framerect.h+=2
		framerect.w+=2
		framerect.x-=1
		framerect.y-=1
	
	return framerect

def getframe(surfrect, resize=0):
	if framestyle!=2:
		framerect=surfrect.inflate(framepad, framepad)
		
	else:
		framerect=surfrect.inflate(1, 1)
		framerect.y-=framepad//2+4
		framerect.h+=framepad//2+4
		framerect.x-=2
		framerect.w+=1
	framerect.y-=hudsize
	framerect.h+=hudsize
	if resize:
		framerect.h+=resizebar
	if framestyle==1:
		framerect.h+=2
		framerect.w+=2
		framerect.x-=1
		framerect.y-=1
	return framerect

def getclose(framerect):
	closebtn=pygame.Rect(framerect.x+framerect.w-2-hudsize, framerect.y+2, hudsize, hudsize)
	return closebtn

def getshade(framerect):
	closebtn=pygame.Rect(framerect.x+framerect.w-2-hudsize-hudsize-2, framerect.y+2, hudsize, hudsize)
	return closebtn


def getpop(framerect):
	poprect=framerect.copy()
	poprect.x-=2
	poprect.y-=2
	poprect.w+=4
	poprect.h+=4
	return poprect


class framex:
	def __init__(self, sizex, sizey, name, xpos=10, ypos=30, resizable=0, sizeminx=140, sizeminy=140, pumpcall=None):
		
		self.shade=0
		#---Required---
		self.resizable=resizable
		self.sizex=sizex
		self.sizey=sizey
		self.xpos=xpos
		self.ypos=ypos
		self.name=name
		if self.ypos<miny:
			self.ypos=miny
		self.wo=None
		self.pid=None
		self.SurfRect=pygame.Rect(self.xpos, self.ypos, sizex, sizey)
		self.framerect=getframe_shadeaware(self, self.SurfRect, self.resizable)
		self.closerect=getclose(self.framerect)
		self.shadrect=getshade(self.framerect)
		self.poprect=getpop(self.framerect)
		self.surface=pygame.Surface((sizex, sizey))
		self.sizeminx=sizeminx
		self.sizeminy=sizeminy
		self.pumpcall=pumpcall
		self.runflg=1
		self.statflg=1
		if self.pumpcall!=None:
			self.pumpcall(self)
		self.statflg=0
		self.tr_lock_reset=None
		#--------------
	def pump(self):
		if self.pumpcall!=None:
			self.pumpcall(self)
		return
	def move(self, xoff, yoff, resetlocks=0):
		self.SurfRect.x-=xoff
		self.SurfRect.y-=yoff
		
		self.xpos-=xoff
		self.ypos-=yoff
		if self.tr_lock_reset!=None:
			if resetlocks==1:
				self.tr_lock_reset=None
			else:	
				self.SurfRect.topright=self.tr_lock_reset
				self.xpos=self.SurfRect.x
		if self.ypos<miny:
			self.ypos=miny
			self.SurfRect.y=miny
		self.framerect=getframe_shadeaware(self, self.SurfRect, self.resizable)
		self.closerect=getclose(self.framerect)
		self.shadrect=getshade(self.framerect)
		self.poprect=getpop(self.framerect)
		return
	def resize(self, xoff, yoff, toprightlock=0):
		if toprightlock:
			self.tr_lock_reset=self.SurfRect.topright
		else:
			self.tr_lock_reset=None
		self.sizex-=xoff
		self.sizey-=yoff
		if self.sizex<self.sizeminx:
			self.sizex=self.sizeminx
			#self.SurfRect.w=self.sizex
		if self.sizey<self.sizeminy:
			self.sizey=self.sizeminy
		self.SurfRect.w=self.sizex
		self.SurfRect.h=self.sizey
		self.surface=pygame.Surface((self.sizex, self.sizey)).convert()
		self.framerect=getframe_shadeaware(self, self.SurfRect, self.resizable)
		self.closerect=getclose(self.framerect)
		self.shadrect=getshade(self.framerect)
		self.poprect=getpop(self.framerect)
		return
	def click(self, event):
		self.statflg=4
		if self.pumpcall!=None:
			self.pumpcall(self, event)
		self.statflg=0
		return
		
	def clickup(self, event):
		self.statflg=5
		if self.pumpcall!=None:
			self.pumpcall(self, event)
		self.statflg=0
		return
	
	
	def keydown(self, event):
		self.statflg=6
		if self.pumpcall!=None:
			self.pumpcall(self, event)
		self.statflg=0
		return
	def keyup(self, event):
		self.statflg=7
		if self.pumpcall!=None:
			self.pumpcall(self, event)
		self.statflg=0
		return
	#calls forwarded to pumpcall using statflg and runflg
	def closecall(self):
		#print("V-PID TERMINATE: " +str(self.pid))
		self.statflg=3
		self.runflg=2
		if self.pumpcall!=None:
			self.pumpcall(self)
		self.statflg=0
	def quitcall(self):
		self.statflg=3
		self.runflg=0
		if self.pumpcall!=None:
			self.pumpcall(self)
		self.statflg=0
	def post_resize(self):
		self.statflg=2
		if self.pumpcall!=None:
			self.pumpcall(self)
		self.statflg=0
	#cleanup function for reopening an existing framex instance.
	#called by framescape automatically.
	def start_prep(self):
		self.statflg=0
		self.runflg=1
	def reshade(self):
		self.statflg=9
		if self.pumpcall!=None:
			self.pumpcall(self)
		self.statflg=0
		self.framerect=getframe_shadeaware(self, self.SurfRect, self.resizable)
		self.closerect=getclose(self.framerect)
		self.shadrect=getshade(self.framerect)
		self.poprect=getpop(self.framerect)
	def unshade(self):
		self.statflg=10
		if self.pumpcall!=None:
			self.pumpcall(self)
		self.statflg=0
		self.framerect=getframe_shadeaware(self, self.SurfRect, self.resizable)
		self.closerect=getclose(self.framerect)
		self.shadrect=getshade(self.framerect)
		self.poprect=getpop(self.framerect)



class ghost:
	def __init__(self, name, pumpcall=None):
		self.name=name
		self.pid=None
		self.wo=0
		self.pumpcall=pumpcall
		self.runflg=1
		self.statflg=1
		if self.pumpcall!=None:
			self.pumpcall(self)
		self.statflg=0
		self.tr_lock_reset=None
		#--------------
	def pump(self):
		if self.pumpcall!=None:
			self.pumpcall(self)
		return
	def click(self, event):
		self.statflg=4
		if self.pumpcall!=None:
			self.pumpcall(self, event)
		self.statflg=0
		return
		
	def clickup(self, event):
		self.statflg=5
		if self.pumpcall!=None:
			self.pumpcall(self, event)
		self.statflg=0
		return
	def keydown(self, event):
		self.statflg=6
		if self.pumpcall!=None:
			self.pumpcall(self, event)
		self.statflg=0
		return
	def keyup(self, event):
		self.statflg=7
		if self.pumpcall!=None:
			self.pumpcall(self, event)
		self.statflg=0
		return
	def closecall(self):
		#print("V-PID TERMINATE: " +str(self.pid))
		self.statflg=3
		self.runflg=2
		if self.pumpcall!=None:
			self.pumpcall(self)
		self.statflg=0
	def quitcall(self):
		self.statflg=3
		self.runflg=0
		if self.pumpcall!=None:
			self.pumpcall(self)
		self.statflg=0
	#cleanup function for reopening an existing ghost instance.
	#called by framescape automatically.
	def start_prep(self):
		self.statflg=0
		self.runflg=1



class desktop:
	def __init__(self, sizex, sizey, name="desktop", bgcolor=(200, 200, 255), pumpcall=None, resizable=0):
		#dummy values
		self.pid=-1
		self.wo=-1
		#---Required---
		self.pumpcall=pumpcall
		self.sizex=sizex
		self.sizey=sizey
		self.name=name
		self.bgcolor=bgcolor
		self.SurfRect=pygame.Rect(0, 0, sizex, sizey)
		self.runflg=1
		self.resizable=resizable
		self.surface=pygame.Surface((sizex, sizey))
		self.surface.fill(bgcolor)
		self.statflg=1
		if self.pumpcall!=None:
			self.pumpcall(self)
		self.statflg=0
		
		self.resizable
	def pump(self):
		if self.pumpcall!=None:
			self.pumpcall(self)
		return
	def keydown(self, event):
		self.statflg=6
		if self.pumpcall!=None:
			self.pumpcall(self, event)
		self.statflg=0
		return
	def keyup(self, event):
		self.statflg=7
		if self.pumpcall!=None:
			self.pumpcall(self, event)
		self.statflg=0
		return
	def click(self, event):
		self.statflg=4
		if self.pumpcall!=None:
			self.pumpcall(self, event)
		self.statflg=0
		return
	def clickup(self, event):
		self.statflg=5
		if self.pumpcall!=None:
			self.pumpcall(self, event)
		self.statflg=0
		return
	def quitcall(self):
		self.statflg=3
		self.runflg=0
		if self.pumpcall!=None:
			self.pumpcall(self)
		self.statflg=0
	def resize(self, xsize, ysize):
		self.sizex=xsize
		self.sizey=ysize
		self.surface=pygame.Surface((xsize, ysize)).convert()
		self.surface.fill(self.bgcolor)
	def post_resize(self):
		self.statflg=8
		if self.pumpcall!=None:
			self.pumpcall(self)
		self.statflg=0
		

color3d=pygame.Color(70, 70, 70)

def draw3Dbox(surface, rect, color1, color2, size=3, invert=0):
	pygame.draw.line(surface, color1, (rect.left, rect.top), (rect.right, rect.top), size)
	pygame.draw.line(surface, color1, (rect.left, rect.top), (rect.left, rect.bottom), size)
	pygame.draw.line(surface, color2, (rect.right, rect.top), (rect.right, rect.bottom), size)
	pygame.draw.line(surface, color2, (rect.left, rect.bottom), (rect.right, rect.bottom), size)

def drawbevelline(surface, color1, color2, point0, point1, size, invert=0):
	point0b=(point0[0], point0[1]-size)
	point1b=(point1[0], point1[1]-size)
	pygame.draw.line(surface, color1, point0, point1, size)
	pygame.draw.line(surface, color2, point0b, point1b, size)


def colorsub(color, mod=color3d):
	try:
		color.r
	except AttributeError:
		color=pygame.Color(color[0], color[1], color[2])
	return color-color3d

def coloradd(color, mod=color3d):
	try:
		color.r
	except AttributeError:
		color=pygame.Color(color[0], color[1], color[2])
	return color+color3d


def framedraw(frame, dispsurf, fg, bg, textcolor, font, abg, atxt, afg, abev, ibev, sub_abev, sub_ibev, sub_bg, add_bg, sub_abg, add_abg):
	framerect=frame.framerect
	poprect=frame.poprect
	closerect=frame.closerect
	shaderect=frame.shadrect
	if frame.wo==0:
		qfg=afg
		qbg=abg
		qtxt=atxt
		bev=abev
		sub_qbg=sub_abg
		add_qbg=add_abg
		sub_bev=sub_abev
	else:
		qfg=fg
		qbg=bg
		qtxt=textcolor
		bev=ibev
		sub_qbg=sub_bg
		add_qbg=add_bg
		sub_bev=sub_ibev
	if not framestyle:
		pygame.draw.rect(dispsurf, qbg, framerect, 0)
		pygame.draw.rect(dispsurf, qfg, framerect, 1)
		pygame.draw.rect(dispsurf, qbg, closerect, 0)
		pygame.draw.line(dispsurf, qfg, closerect.topleft, closerect.bottomright, 1)
		pygame.draw.line(dispsurf, qfg, closerect.topright, closerect.bottomleft, 1)
		pygame.draw.rect(dispsurf, qfg, closerect, 1)
		pygame.draw.rect(dispsurf, qbg, shaderect, 0)
		pygame.draw.line(dispsurf, qfg, shaderect.midleft, shaderect.midright, 1)
		pygame.draw.rect(dispsurf, qfg, shaderect, 1)
		if frame.resizable:
			pygame.draw.line(dispsurf, qfg, (framerect.x, framerect.y+framerect.h-(resizebar//2)-(resizebar//3)), (framerect.x+(framerect.w-1), framerect.y+framerect.h-(resizebar//2)-(resizebar//3)))
			pygame.draw.line(dispsurf, qfg, (framerect.x+(framerect.w//2), framerect.y+framerect.h-(resizebar)-framepad), (framerect.x+(framerect.w//2), framerect.y+framerect.h-1), 2)
			pygame.draw.line(dispsurf, qfg, (framerect.x, framerect.y+framerect.h-(resizebar//2)), (framerect.x+(framerect.w-1), framerect.y+framerect.h-(resizebar//2)), 2)
	elif framestyle==2:
		#3D frame style 2
		pygame.draw.rect(dispsurf, qbg, framerect, 0)
		if frame.resizable:
			#pygame.draw.line(dispsurf, qfg, (framerect.x, framerect.y+framerect.h-(resizebar//2)-(resizebar//3)), (framerect.x+(framerect.w-1), framerect.y+framerect.h-(resizebar//2)-(resizebar//3)))
			pygame.draw.line(dispsurf, qfg, (framerect.x+(framerect.w//2), framerect.y+framerect.h-(resizebar)-framepad), (framerect.x+(framerect.w//2), framerect.y+framerect.h-1), 2)
			#pygame.draw.line(dispsurf, qfg, (framerect.x, framerect.y+framerect.h-(resizebar//2)), (framerect.x+(framerect.w-1), framerect.y+framerect.h-(resizebar//2)), 2)
		draw3Dbox(dispsurf, poprect, bev, sub_bev, 2)
		draw3Dbox(dispsurf, framerect, sub_bev, bev, 2)
		pygame.draw.rect(dispsurf, qbg, closerect, 0)
		pygame.draw.line(dispsurf, qfg, closerect.topleft, closerect.bottomright, 2)
		pygame.draw.line(dispsurf, qfg, closerect.topright, closerect.bottomleft, 2)
		draw3Dbox(dispsurf, closerect, add_qbg, sub_qbg, 2)
		pygame.draw.rect(dispsurf, qbg, shaderect, 0)
		pygame.draw.line(dispsurf, qfg, shaderect.midleft, shaderect.midright, 2)
		draw3Dbox(dispsurf, shaderect, add_qbg, sub_qbg, 2)
		drawbevelline(dispsurf, sub_bev, bev, (framerect.x+2, frame.ypos-2), (framerect.x+framerect.w-1, frame.ypos-2), 2, 1)
		
	else:
		#3D frame style
		pygame.draw.rect(dispsurf, qbg, framerect, 0)
		if frame.resizable:
			pygame.draw.line(dispsurf, qfg, (framerect.x, framerect.y+framerect.h-(resizebar//2)-(resizebar//3)), (framerect.x+(framerect.w-1), framerect.y+framerect.h-(resizebar//2)-(resizebar//3)))
			pygame.draw.line(dispsurf, qfg, (framerect.x+(framerect.w//2), framerect.y+framerect.h-(resizebar)-framepad), (framerect.x+(framerect.w//2), framerect.y+framerect.h-1), 2)
			pygame.draw.line(dispsurf, qfg, (framerect.x, framerect.y+framerect.h-(resizebar//2)), (framerect.x+(framerect.w-1), framerect.y+framerect.h-(resizebar//2)), 2)
		draw3Dbox(dispsurf, framerect, add_qbg, sub_qbg)
		pygame.draw.rect(dispsurf, qbg, closerect, 0)
		pygame.draw.line(dispsurf, qfg, closerect.topleft, closerect.bottomright, 2)
		pygame.draw.line(dispsurf, qfg, closerect.topright, closerect.bottomleft, 2)
		draw3Dbox(dispsurf, closerect, add_qbg, sub_qbg, 2)
		pygame.draw.rect(dispsurf, qbg, shaderect, 0)
		pygame.draw.line(dispsurf, qfg, shaderect.midleft, shaderect.midright, 2)
		draw3Dbox(dispsurf, shaderect, add_qbg, sub_qbg, 2)
	if frame.wo==0:
		if frame.name not in titlecacheact:
			namex=font.render(frame.name, True, atxt, abg).convert()
			titlecacheact[frame.name]=namex
		else:
			namex=titlecacheact[frame.name]
	else:
		if frame.name not in titlecache:
			namex=font.render(frame.name, True, textcolor, bg).convert()
			titlecache[frame.name]=namex
		else:
			namex=titlecache[frame.name]
	namexrect=namex.get_rect()
	if namexrect.w>framerect.w-8-hudsize-hudsize:
		namexrect.w=framerect.w-8-hudsize-hudsize
	else:
		namexrect=None
	dispsurf.blit(namex, (framerect.x+2, framerect.y+2), area=namexrect)
	dispsurf.blit(frame.surface, frame.SurfRect)


def shadedraw(frame, dispsurf, fg, bg, textcolor, font, abg, atxt, afg, abev, ibev, sub_abev, sub_ibev, sub_bg, add_bg, sub_abg, add_abg):
	framerect=frame.framerect
	poprect=frame.poprect
	closerect=frame.closerect
	shaderect=frame.shadrect
	if frame.wo==0:
		qfg=afg
		qbg=abg
		qtxt=atxt
		bev=abev
		sub_qbg=sub_abg
		add_qbg=add_abg
		sub_bev=sub_abev
	else:
		qfg=fg
		qbg=bg
		qtxt=textcolor
		bev=ibev
		sub_qbg=sub_bg
		add_qbg=add_bg
		sub_bev=sub_ibev
	if not framestyle:
		pygame.draw.rect(dispsurf, qbg, framerect, 0)
		pygame.draw.rect(dispsurf, qfg, framerect, 1)
		pygame.draw.rect(dispsurf, qbg, closerect, 0)
		pygame.draw.line(dispsurf, qfg, closerect.topleft, closerect.bottomright, 1)
		pygame.draw.line(dispsurf, qfg, closerect.topright, closerect.bottomleft, 1)
		pygame.draw.rect(dispsurf, qfg, closerect, 1)
		pygame.draw.rect(dispsurf, qbg, shaderect, 0)
		pygame.draw.line(dispsurf, qfg, shaderect.midleft, shaderect.midright, 1)
		pygame.draw.rect(dispsurf, qfg, shaderect, 1)
		#if frame.resizable:
		#	pygame.draw.line(dispsurf, qfg, (framerect.x, framerect.y+framerect.h-(resizebar//2)-(resizebar//3)), (framerect.x+(framerect.w-1), framerect.y+framerect.h-(resizebar//2)-(resizebar//3)))
		#	pygame.draw.line(dispsurf, qfg, (framerect.x+(framerect.w//2), framerect.y+framerect.h-(resizebar)-framepad), (framerect.x+(framerect.w//2), framerect.y+framerect.h-1), 2)
		#	pygame.draw.line(dispsurf, qfg, (framerect.x, framerect.y+framerect.h-(resizebar//2)), (framerect.x+(framerect.w-1), framerect.y+framerect.h-(resizebar//2)), 2)
	elif framestyle==2:
		#3D frame style 2
		pygame.draw.rect(dispsurf, qbg, framerect, 0)
		#if frame.resizable:
		#	#pygame.draw.line(dispsurf, qfg, (framerect.x, framerect.y+framerect.h-(resizebar//2)-(resizebar//3)), (framerect.x+(framerect.w-1), framerect.y+framerect.h-(resizebar//2)-(resizebar//3)))
		#	pygame.draw.line(dispsurf, qfg, (framerect.x+(framerect.w//2), framerect.y+framerect.h-(resizebar)-framepad), (framerect.x+(framerect.w//2), framerect.y+framerect.h-1), 2)
		#	#pygame.draw.line(dispsurf, qfg, (framerect.x, framerect.y+framerect.h-(resizebar//2)), (framerect.x+(framerect.w-1), framerect.y+framerect.h-(resizebar//2)), 2)
		draw3Dbox(dispsurf, poprect, bev, sub_bev, 2)
		draw3Dbox(dispsurf, framerect, sub_bev, bev, 2)
		pygame.draw.rect(dispsurf, qbg, closerect, 0)
		pygame.draw.line(dispsurf, qfg, closerect.topleft, closerect.bottomright, 2)
		pygame.draw.line(dispsurf, qfg, closerect.topright, closerect.bottomleft, 2)
		draw3Dbox(dispsurf, closerect, add_qbg, sub_qbg, 2)
		pygame.draw.rect(dispsurf, qbg, shaderect, 0)
		pygame.draw.line(dispsurf, qfg, shaderect.midleft, shaderect.midright, 2)
		draw3Dbox(dispsurf, shaderect, add_qbg, sub_qbg, 2)
		#drawbevelline(dispsurf, qfg, (framerect.x+2, frame.ypos-2), (framerect.x+framerect.w-1, frame.ypos-2), 2, 1)
		
	else:
		#3D frame style
		pygame.draw.rect(dispsurf, qbg, framerect, 0)
		#if frame.resizable:
		#	pygame.draw.line(dispsurf, qfg, (framerect.x, framerect.y+framerect.h-(resizebar//2)-(resizebar//3)), (framerect.x+(framerect.w-1), framerect.y+framerect.h-(resizebar//2)-(resizebar//3)))
		#	pygame.draw.line(dispsurf, qfg, (framerect.x+(framerect.w//2), framerect.y+framerect.h-(resizebar)-framepad), (framerect.x+(framerect.w//2), framerect.y+framerect.h-1), 2)
		#	pygame.draw.line(dispsurf, qfg, (framerect.x, framerect.y+framerect.h-(resizebar//2)), (framerect.x+(framerect.w-1), framerect.y+framerect.h-(resizebar//2)), 2)
		draw3Dbox(dispsurf, framerect, add_qbg, sub_qbg)
		pygame.draw.rect(dispsurf, qbg, closerect, 0)
		pygame.draw.line(dispsurf, qfg, closerect.topleft, closerect.bottomright, 2)
		pygame.draw.line(dispsurf, qfg, closerect.topright, closerect.bottomleft, 2)
		draw3Dbox(dispsurf, closerect, add_qbg, sub_qbg, 2)
		pygame.draw.rect(dispsurf, qbg, shaderect, 0)
		pygame.draw.line(dispsurf, qfg, shaderect.midleft, shaderect.midright, 2)
		draw3Dbox(dispsurf, shaderect, add_qbg, sub_qbg, 2)
	if frame.wo==0:
		if frame.name not in titlecacheact:
			namex=font.render(frame.name, True, atxt, abg).convert()
			titlecacheact[frame.name]=namex
		else:
			namex=titlecacheact[frame.name]
	else:
		if frame.name not in titlecache:
			namex=font.render(frame.name, True, textcolor, bg).convert()
			titlecache[frame.name]=namex
		else:
			namex=titlecache[frame.name]
	namexrect=namex.get_rect()
	if namexrect.w>framerect.w-8-hudsize-hudsize:
		namexrect.w=framerect.w-8-hudsize-hudsize
	else:
		namexrect=None
	dispsurf.blit(namex, (framerect.x+2, framerect.y+2), area=namexrect)
	#dispsurf.blit(frame.surface, frame.SurfRect)

class framescape:
	def __init__(self, desktop, framebg=(110, 110, 130), framefg=(255, 255, 255), frametext=(255, 255, 255), actframebg=(0, 100, 130), actframefg=(255, 255, 255), actframetext=(255, 255, 255), actbevel=(255, 255, 255), inactbevel=(255, 255, 255), deskicon=None):
		if deskicon!=None:
			pygame.display.set_icon(deskicon)
		if desktop.resizable:
			self.surface=pygame.display.set_mode((desktop.sizex, desktop.sizey), pygame.RESIZABLE)
		else:
			self.surface=pygame.display.set_mode((desktop.sizex, desktop.sizey))
		self.proclist=[]
		self.idlook={}
		self.idcnt=0
		self.desktop=desktop
		self.ghostproc=[]
		pygame.display.set_caption(desktop.name, desktop.name)
		self.desktop.surface.convert(self.surface)
		self.moveframe=None
		self.clock=pygame.time.Clock()
		self.runflg=1
		self.fbg=framebg
		self.ffg=framefg
		self.afbg=actframebg
		self.affg=actframefg
		self.sub_fbg=colorsub(framebg)
		self.add_fbg=coloradd(framebg)
		self.sub_afbg=colorsub(actframebg)
		self.add_afbg=coloradd(actframebg)
		self.abev=actbevel
		self.iabev=inactbevel
		self.sub_abev=colorsub(actbevel)
		self.sub_iabev=colorsub(inactbevel)
		self.ftxt=frametext
		self.aftxt=actframetext
		self.resizedesk=0
		self.activeframe=None
		self.simplefont = pygame.font.SysFont(None, fontsize)
		print("Strazoloid Window Manager v1.2.1")
	def close_pid(self, pid):
		try:
			frame=self.idlook[pid]
			if frame in self.proclist:
				self.proclist.remove(frame)
				if frame==self.activeframe:
					self.activeframe=None
					for framew in self.proclist:
						framew.wo-=1
						if framew.wo==0:
							self.activeframe=framew
				frame.closecall()
			
			if frame in self.ghostproc:
				self.ghostproc.remove(frame)
				frame.closecall()
		except KeyError:
			return
	def close_frame(self, frame):
		if frame in self.proclist:
			self.proclist.remove(frame)
			if frame==self.activeframe:
				self.activeframe=None
				for framew in self.proclist:
					framew.wo-=1
					if framew.wo==0:
						self.activeframe=framew
			frame.closecall()
	def close_ghost(self, ghost):
		if ghost in self.ghostproc:
			self.ghostproc.remove(ghost)
			ghost.closecall()
	def add_frame(self, frame):
		frame.surface.convert(self.surface)
		frame.start_prep()
		frame.pid=self.idcnt
		self.idcnt+=1
		for framew in self.proclist:
			framew.wo+=1
		frame.wo=0
		self.activeframe=frame
		self.proclist.extend([frame])
		self.idlook[frame.pid]=frame
	def add_ghost(self, ghost):
		ghost.start_prep()
		ghost.pid=self.idcnt
		self.idcnt+=1
		
		self.ghostproc.extend([ghost])
		self.idlook[ghost.pid]=ghost
		
	def process(self):
		while self.runflg:
			cachesizecheck()
			
			if self.resizedesk==1:
				self.resizedesk=2
			elif self.resizedesk==2:
				self.resizedesk=0
				if resw<300:
					resw=300
				if resh<300:
					resh=300
				self.desktop.resize(resw, resh)
				self.surface=pygame.display.set_mode((self.desktop.sizex, self.desktop.sizey), pygame.RESIZABLE)
				self.desktop.post_resize()
			self.clock.tick(wmfps)
			#pump calls
			self.desktop.pump()
			for frame in self.proclist:
				frame.pump()
			for ghost in self.ghostproc:
				ghost.pump()
			#move & resize
			if self.moveframe!=None:
				prevpos=movepos
				movepos=pygame.mouse.get_pos()
				xoff =(prevpos[0] - movepos[0])
				yoff =(prevpos[1] - movepos[1])
				#normal resize
				if resizeframe==1:
					self.moveframe.resize(xoff, yoff)
				#inverted resize
				elif resizeframe==2:
					self.moveframe.resize(-xoff, yoff, 1)
					self.moveframe.move(xoff, 0)
				#regular move
				else:	
					self.moveframe.move(xoff, yoff, 1)
			#dispay render
			self.proclist.sort(key=lambda x: x.wo, reverse=True)
			self.surface.blit(self.desktop.surface, (0, 0))
			for frame in self.proclist:
				if frame.shade:
					shadedraw(frame, self.surface, self.ffg, self.fbg, self.ftxt, self.simplefont, self.afbg, self.aftxt, self.affg, self.abev, self.iabev, self.sub_abev, self.sub_iabev, self.sub_fbg, self.add_fbg, self.sub_afbg, self.add_afbg)
				else:
					framedraw(frame, self.surface, self.ffg, self.fbg, self.ftxt, self.simplefont, self.afbg, self.aftxt, self.affg, self.abev, self.iabev, self.sub_abev, self.sub_iabev, self.sub_fbg, self.add_fbg, self.sub_afbg, self.add_afbg)
					
				
			pygame.display.flip()
			#event parser
			for event in pygame.event.get():
				if event.type==pygame.VIDEORESIZE:
					self.resizedesk=1
					resw=event.w
					resh=event.h
					time.sleep(0.1)
					break
				if event.type==pygame.QUIT:
					self.runflg=0
					for frame in self.proclist:
						frame.quitcall()
					for ghost in self.ghostproc:
						ghost.quitcall()
					self.desktop.quitcall()
					
					break
				if event.type==pygame.KEYDOWN:
					if self.activeframe!=None:
						self.activeframe.keydown(event)
					self.desktop.keydown(event)
					for ghost in self.ghostproc:
						ghost.keydown(event)
				if event.type==pygame.KEYUP:
					if self.activeframe!=None:
						self.activeframe.keyup(event)
					self.desktop.keyup(event)
					for ghost in self.ghostproc:
						ghost.keyup(event)
				if event.type==pygame.MOUSEBUTTONUP:
					if event.button==1:
						if self.moveframe!=None and resizeframe!=0:
							self.moveframe.post_resize()
						self.moveframe=None
					if self.activeframe!=None:
						self.activeframe.clickup(event)
					self.desktop.clickup(event)
					for ghost in self.ghostproc:
						ghost.clickup(event)
				if event.type==pygame.MOUSEBUTTONDOWN:
					self.proclist.sort(key=lambda x: x.wo, reverse=False)
					for ghost in self.ghostproc:
						ghost.click(event)
					click=0
					for frame in self.proclist:
						framerectx=getframe_shadeaware(frame, frame.SurfRect, frame.resizable)
						if framerectx.collidepoint(event.pos):
							if frame.SurfRect.collidepoint(event.pos) and frame.shade==0:
								if frame.wo==0:
									frame.click(event)
									click=1
									break
								click=1
								if frame.wo!=None:
									for framew in self.proclist:
										framew.wo+=1
									frame.wo=0
									self.activeframe=frame
									frame.click(event)
									break
							elif getclose(framerectx).collidepoint(event.pos) and event.button==1:
								self.proclist.remove(frame)
								frame.closecall()
								if frame==self.activeframe:
									self.activeframe=None
									for framew in self.proclist:
										framew.wo-=1
										if framew.wo==0:
											self.activeframe=framew
								break
							elif getshade(framerectx).collidepoint(event.pos) and event.button==1:
								if frame.shade:
									frame.shade=0
									frame.unshade()
								else:
									frame.shade=1
									frame.reshade()
								break
							elif event.button==5:
								if frame.shade:
									frame.shade=0
									frame.unshade()
								break
							elif event.button==4:
								if not frame.shade:
									frame.shade=1
									frame.reshade()
								break
							elif event.button==1:
								if event.pos[1]>frame.ypos+framepad+hudsize and frame.resizable:
									if event.pos[0]<frame.xpos+(frame.sizex//2):
										resizeframe=2
									else:
										resizeframe=1
								else:
									resizeframe=0
								self.moveframe=frame
								movepos=event.pos
								click=1
								if frame.wo!=None:
									for framew in self.proclist:
										framew.wo+=1
									frame.wo=0
									self.activeframe=frame
									break
					if click==0:
						self.desktop.click(event)
						
					
		