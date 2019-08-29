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
import random

simplefont = pygame.font.SysFont(libzox.cnfdict["menufont"], int(libzox.cnfdict["menufontsize"]))

framesc=None

diag_yes=pygame.image.load(os.path.join(libzox.gfxpath, "diag_yes.png"))
diag_no=pygame.image.load(os.path.join(libzox.gfxpath, "diag_no.png"))
clock_wicon=pygame.image.load(os.path.join(libzox.gfxpath, "clock_wicon.png"))
tip_wicon=pygame.image.load(os.path.join(libzox.gfxpath, "tip_wicon.png"))
sinfo_wicon=pygame.image.load(os.path.join(libzox.gfxpath, "sinfo_wicon.png"))
yn_wicon=pygame.image.load(os.path.join(libzox.gfxpath, "yn_wicon.png"))
about_wicon=pygame.image.load(os.path.join(libzox.gfxpath, "about_wicon.png"))



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
		frameobj.surface.fill((220, 220, 220))
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
			frameobj.seticon(yn_wicon.convert())
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
		self.soundspath=os.path.join("vgop", "sounds")
		self.hourding=pygame.mixer.Sound(os.path.join(self.soundspath, "clockhour.ogg"))
		self.minding=pygame.mixer.Sound(os.path.join(self.soundspath, "clockmin.ogg"))
		self.tform="%I:%M %p"
		self.dform="%A, %B %d, %Y"
		self.fonttime=pygame.font.SysFont(None, 30)
		self.font=pygame.font.SysFont(None, 22)
		
	def renderdisp(self, frameobj):
		frameobj.surface.fill((223, 223, 223))
		self.ypos=0
		if self.timest.startswith("0"):
			timetx=self.fonttime.render(self.timest[1:], True, (0, 0, 0), (223, 223, 223))
			frameobj.name=self.timest[1:]+" - Clock"
		else:
			timetx=self.fonttime.render(self.timest, True, (0, 0, 0), (223, 223, 223))
			frameobj.name=self.timest+" - Clock"
		datetx=self.font.render(self.datest, True, (0, 0, 0), (223, 223, 223))
		timexpos=frameobj.surface.get_width()//2 - timetx.get_width()//2
		datexpos=frameobj.surface.get_width()//2 - datetx.get_width()//2
		frameobj.surface.blit(timetx, (timexpos, 2))
		frameobj.surface.blit(datetx, (datexpos, 34))
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==1:
			frameobj.name="Clock"
			frameobj.seticon(clock_wicon.convert())
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
		sv=sys.version_info
		items=["Open Windows : " + str(len(framesc.proclist)),
		"gopher-gets: " + str(len(libgop.socketlist)),
		"------:------",
		"python ver: v" + str(sv[0]) + "." + str(sv[1]) + "." + str(sv[2]) + "." + str(sv[3]) + "." + str(sv[4]),
		"pygame ver: v" + pygame.version.ver,
		"OS Family: " + os.name,
		"OS: " + sys.platform]
		for item in items:
			itema, itemb = item.split(":", 1)
			
			itemtxA=self.font.render(itema+":", True, (0, 0, 0), (223, 223, 223))
			itemtxB=self.font.render(itemb, True, (0, 0, 0), (223, 223, 223))
			itemxposB=frameobj.surface.get_width()- itemtxB.get_width()
			frameobj.surface.blit(itemtxA, (0, self.ypos))
			frameobj.surface.blit(itemtxB, (itemxposB, self.ypos))
			
			self.ypos+=22
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==1:
			frameobj.name="System Info"
			self.renderdisp(frameobj)
			frameobj.seticon(sinfo_wicon.convert())
			self.ticker=libzox.tickdo(5)
		if frameobj.statflg==0:
			if self.ticker.tick():
				self.renderdisp(frameobj)

class tipofday:
	def __init__(self):
		self.font=pygame.font.SysFont(None, 22)
		self.tips=[]
		self.tipload()
	def tipload(self):
		pathis=["libzoxphr", "dat", "tipofday.dat"]
		t=open(os.path.join(*pathis), "r")
		for line in t:
			self.tips.extend([line.replace("\n", "")])
		self.tipmax=len(self.tips)-1
	def renderdisp(self, frameobj):
		frameobj.name="Tip Of The Day #" + str(self.tindex+1)
		frameobj.surface.fill((223, 223, 255))
		textitem(self.tips[self.tindex], self.font, 22, (0, 0, 0), frameobj.surface, 0, {}, xoff=0, textcoly=(223, 223, 255))

	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==0 and frameobj.wo==0:
			mpos=pygame.mouse.get_pos()
			if frameobj.SurfRect.collidepoint(mpos):
				deskt.hovertext="Leftclick for next tip. Rightclick for previous tip."
		if frameobj.statflg==1:
			self.tindex=random.randint(0, self.tipmax)
			self.renderdisp(frameobj)
			frameobj.seticon(tip_wicon.convert())
		if frameobj.statflg==4:
			if data.button==1:
				self.tindex+=1
				if self.tindex>self.tipmax:
					self.tindex=0
				self.renderdisp(frameobj)
			if data.button==3:
				self.tindex-=1
				if self.tindex<0:
					self.tindex=self.tipmax
				self.renderdisp(frameobj)

versionstring='Version: v3.0.0.indev - Codename: "Par 12"'

class aboutsplash:
	def __init__(self):
		self.font=pygame.font.SysFont(None, 22)
		if "indev" in versionstring:
			self.splashbg=pygame.image.load(os.path.join(libzox.gfxpath, "aboutsplash_indev.jpg")).convert()

		else:
			self.splashbg=pygame.image.load(os.path.join(libzox.gfxpath, "aboutsplash.jpg")).convert()
	def renderdisp(self, frameobj):
		#frameobj.surface.fill((255, 255, 255))
		frameobj.surface.blit(self.splashbg, (0, 0))
		frameobj.surface.blit(self.versiontext, (self.versionpos))
	def pumpcall1(self, frameobj, data=None):
		#if frameobj.statflg==0:
		#	self.renderdisp(frameobj)
		if frameobj.statflg==1:
			self.versiontext=self.font.render(versionstring, True, (0, 0, 0))
			self.versionpos=(frameobj.surface.get_width()-self.versiontext.get_width(), frameobj.surface.get_height()-self.versiontext.get_height())
			frameobj.seticon(about_wicon.convert())
			frameobj.name=versionstring
			self.renderdisp(frameobj)

