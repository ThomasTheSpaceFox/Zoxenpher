#!/usr/bin/env python
#import time
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