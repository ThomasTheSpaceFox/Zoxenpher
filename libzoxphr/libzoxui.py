#!/usr/bin/env python
import time
import os
import sys
from . import libgop
import pygame
from threading import Thread
from . import strazoloidwm as stz
from . import libzox
from .libzox import progobj
from .libzox import textitem

simplefont = pygame.font.SysFont(libzox.cnfdict["menufont"], int(libzox.cnfdict["menufontsize"]))

framesc=None

diag_yes=pygame.image.load(os.path.join("vgop", "diag_yes.png"))
diag_no=pygame.image.load(os.path.join("vgop", "diag_no.png"))

def init(framescape, desktop):
	global framesc
	global deskt
	framesc=framescape
	deskt=desktop

def do_yndialog(name, message, callback, canclose=0, carrydata=None):
	newgop=yndialog(name, message, callback, canclose, carrydata)
	framesc.add_frame(stz.framex(400, 150, name, resizable=0, pumpcall=newgop.pumpcall1, xpos=60, ypos=100))


class yndialog:
	def __init__(self, name, message, callback, canclose, carrydata=None):
		self.canclose=canclose
		self.ypos=0
		self.yjump=int(libzox.cnfdict["menutextjump"])
		self.dname=name
		self.message=message
		self.callback=callback
		self.carrydata=carrydata
	def renderdisp(self, frameobj):
		frameobj.surface.fill((223, 223, 223))
		for line in self.message.split("\n"):
			foo, self.ypos, bar = textitem(line, simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.ypos, {}, xoff=0, textcoly=(223, 223, 223))
		
		centerx=frameobj.surface.get_width()//2
		
		yesx=centerx-diag_yes.get_width()-5
		nox=centerx+5
		yesnoy=frameobj.surface.get_height()-diag_yes.get_height()-4
		
		self.yrect=frameobj.surface.blit(diag_yes, (yesx, yesnoy))
		self.nrect=frameobj.surface.blit(diag_no, (nox, yesnoy))
		
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==2:
			self.renderdisp(frameobj)
		if frameobj.statflg==1:
			frameobj.name=self.dname
			self.renderdisp(frameobj)
		if frameobj.statflg==3:
			if frameobj.runflg==2:
				if not self.canclose:
					framesc.add_frame(frameobj)
			else:
				self.callback(0, self.carrydata)
				framesc.close_frame(frameobj)
		if frameobj.statflg==4:
			if data.button==1:
				if self.yrect.collidepoint(stz.mousehelper(data.pos, frameobj)):
					self.callback(1, self.carrydata)
					framesc.close_frame(frameobj)
				if self.nrect.collidepoint(stz.mousehelper(data.pos, frameobj)):
					self.callback(0, self.carrydata)
					framesc.close_frame(frameobj)
		if frameobj.statflg==6:
			if data.key==pygame.K_y:
				self.callback(1, self.carrydata)
				framesc.close_frame(frameobj)
			elif data.key==pygame.K_n:
				self.callback(0, self.carrydata)
				framesc.close_frame(frameobj)


class clock:
	def __init__(self):
		self.ypos=0
		self.hourding=pygame.mixer.Sound(os.path.join("vgop", "clockhour.ogg"))
		self.minding=pygame.mixer.Sound(os.path.join("vgop", "clockmin.ogg"))
		self.tform="%I:%M %p"
		self.dform="%A, %B %H, %Y"
		self.fonttime=pygame.font.SysFont(None, 30)
		self.font=pygame.font.SysFont(None, 22)
		
	def renderdisp(self, frameobj):
		frameobj.surface.fill((223, 223, 223))
		self.ypos=0
		timetx=self.fonttime.render(self.timest, True, (0, 0, 0), (223, 223, 223))
		datetx=self.font.render(self.datest, True, (0, 0, 0), (223, 223, 223))
		timexpos=frameobj.surface.get_width()//2 - timetx.get_width()//2
		datexpos=frameobj.surface.get_width()//2 - datetx.get_width()//2
		frameobj.surface.blit(timetx, (timexpos, 2))
		frameobj.surface.blit(datetx, (datexpos, 34))
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==1:
			frameobj.name="Clock"
			self.time=time.localtime()
			self.hour=self.time.tm_hour
			self.minu=self.time.tm_min
			self.timest=time.strftime(self.tform, self.time)
			self.datest=time.strftime(self.dform, self.time)
			self.renderdisp(frameobj)
		if frameobj.statflg==0:
			self.time=time.localtime()
			if self.time.tm_hour!=self.hour and self.time.tm_min==0:
				self.hourding.play()
			if self.time.tm_min!=self.minu:
				self.minding.play()
			if self.time.tm_min!=self.minu:
				self.hour=self.time.tm_hour
				self.minu=self.time.tm_min
				self.timest=time.strftime(self.tform, self.time)
				self.datest=time.strftime(self.dform, self.time)
				self.renderdisp(frameobj)




class sinfo:
	def __init__(self):
		self.ypos=0
		self.hourding=pygame.mixer.Sound(os.path.join("vgop", "clockhour.ogg"))
		self.minding=pygame.mixer.Sound(os.path.join("vgop", "clockmin.ogg"))
		self.font=pygame.font.SysFont(None, 22)
		
	def renderdisp(self, frameobj):
		frameobj.surface.fill((223, 223, 223))
		self.ypos=0
		for item in ["Open Windows : " + str(len(framesc.proclist)), "gopher-gets: " + str(len(libgop.socketlist))]:
			itemtx=self.font.render(item, True, (0, 0, 0), (223, 223, 223))
			itemxpos=frameobj.surface.get_width()//2 - itemtx.get_width()//2
			frameobj.surface.blit(itemtx, (itemxpos, self.ypos))
			self.ypos+=22
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==1:
			frameobj.name="System Info"
			self.renderdisp(frameobj)
			self.ticker=libzox.tickdo(5)
		if frameobj.statflg==0:
			if self.ticker.tick():
				self.renderdisp(frameobj)