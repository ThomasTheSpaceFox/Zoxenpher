#!/usr/bin/env python
import os
import pygame
import time
import math
pygame.display.init()
pygame.font.init()
#ui stiling globals
framepad=8
hudsize=20
fontsize=25

resizebar=10

titlecache={}
titlecacheact={}


def mousehelper(mpos, frameobj):
	return (mpos[0]-frameobj.xpos, mpos[1]-frameobj.ypos)

def getframe(surfrect, resize=0):
	framerect=surfrect.inflate(framepad, framepad)
	framerect.y-=hudsize
	framerect.h+=hudsize
	if resize:
		framerect.h+=resizebar
	return framerect

def getclose(framerect):
	closebtn=pygame.Rect(framerect.x, framerect.y, hudsize, hudsize)
	return closebtn

class framex:
	def __init__(self, sizex, sizey, name, xpos=10, ypos=30, resizable=0, sizeminx=140, sizeminy=140, pumpcall=None):
		
		
		#---Required---
		self.resizable=resizable
		self.sizex=sizex
		self.sizey=sizey
		self.xpos=xpos
		self.ypos=ypos
		self.name=name
		self.wo=None
		self.pid=None
		self.SurfRect=pygame.Rect(xpos, ypos, sizex, sizey)
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
		
def framedraw(frame, dispsurf, fg, bg, textcolor, font, abg, atxt, afg):
	framerect=getframe(frame.SurfRect, frame.resizable)
	closerect=getclose(framerect)
	
	if frame.wo==0:
		qfg=afg
		qbg=abg
		qtxt=atxt
	else:
		qfg=fg
		qbg=bg
		qtxt=textcolor
	pygame.draw.rect(dispsurf, qbg, framerect, 0)
	pygame.draw.rect(dispsurf, qfg, framerect, 1)
	pygame.draw.rect(dispsurf, qbg, closerect, 0)
	pygame.draw.rect(dispsurf, qfg, closerect, 1)
	
	
	if frame.resizable:
		pygame.draw.line(dispsurf, qfg, (framerect.x, framerect.y+framerect.h-(resizebar//2)-(resizebar//3)), (framerect.x+(framerect.w-1), framerect.y+framerect.h-(resizebar//2)-(resizebar//3)))
		pygame.draw.line(dispsurf, qfg, (framerect.x+(framerect.w//2), framerect.y+framerect.h-(resizebar)-framepad), (framerect.x+(framerect.w//2), framerect.y+framerect.h-1), 2)
		pygame.draw.line(dispsurf, qfg, (framerect.x, framerect.y+framerect.h-(resizebar//2)), (framerect.x+(framerect.w-1), framerect.y+framerect.h-(resizebar//2)), 2)
	if frame.wo==0:
		if frame.name not in titlecacheact:
			namex=font.render(frame.name, True, atxt, abg)
			titlecacheact[frame.name]=namex
		else:
			namex=titlecacheact[frame.name]
	else:
		if frame.name not in titlecache:
			namex=font.render(frame.name, True, textcolor, bg)
			titlecache[frame.name]=namex
		else:
			namex=titlecache[frame.name]
	dispsurf.blit(namex, (framerect.x+hudsize+2, framerect.y+1))
	dispsurf.blit(frame.surface, frame.SurfRect)

class framescape:
	def __init__(self, desktop, framebg=(110, 110, 130), framefg=(255, 255, 255), frametext=(255, 255, 255), actframebg=(0, 100, 130), actframefg=(255, 255, 255), actframetext=(255, 255, 255), deskicon=None):
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
		
		pygame.display.set_caption(desktop.name, desktop.name)
		self.desktop.surface.convert(self.surface)
		self.moveframe=None
		self.clock=pygame.time.Clock()
		self.runflg=1
		self.fbg=framebg
		self.ffg=framefg
		self.afbg=actframebg
		self.affg=actframefg
		self.ftxt=frametext
		self.aftxt=actframetext
		self.resizedesk=0
		self.activeframe=None
		self.simplefont = pygame.font.SysFont(None, fontsize)
		print("Strazoloid Window Manager v1.0.2")
	def close_pid(self, pid):
		try:
			frame=self.idlook[pid]
			if frame in self.proclist:
				self.proclist.remove(frame)
				frame.closecall()
		except KeyError:
			return
	def close_frame(self, frame):
		if frame in self.proclist:
			self.proclist.remove(frame)
			frame.closecall()
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
	def process(self):
		while self.runflg:
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
			self.clock.tick(30)
			#pump calls
			self.desktop.pump()
			for frame in self.proclist:
				frame.pump()
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
				framedraw(frame, self.surface, self.ffg, self.fbg, self.ftxt, self.simplefont, self.afbg, self.aftxt, self.affg)
				
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
					self.desktop.quitcall()
					break
				if event.type==pygame.KEYDOWN:
					if self.activeframe!=None:
						self.activeframe.keydown(event)
					self.desktop.keydown(event)
				if event.type==pygame.KEYUP:
					if self.activeframe!=None:
						self.activeframe.keyup(event)
					self.desktop.keyup(event)
				if event.type==pygame.MOUSEBUTTONUP:
					if event.button==1:
						if self.moveframe!=None and resizeframe!=0:
							self.moveframe.post_resize()
						self.moveframe=None
					if self.activeframe!=None:
						self.activeframe.clickup(event)
					self.desktop.clickup(event)
				if event.type==pygame.MOUSEBUTTONDOWN:
					self.proclist.sort(key=lambda x: x.wo, reverse=False)
					
					click=0
					for frame in self.proclist:
						framerectx=getframe(frame.SurfRect, frame.resizable)
						if framerectx.collidepoint(event.pos):
							if frame.SurfRect.collidepoint(event.pos):
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
									break
							elif getclose(framerectx).collidepoint(event.pos) and event.button==1:
								self.proclist.remove(frame)
								frame.closecall()
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
						
					
		