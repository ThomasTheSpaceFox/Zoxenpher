#!/usr/bin/env python
#import time
import os
import libgop
import pygame
from threading import Thread
import strazoloidwm as stz
#import copy
print("Zoxenpher v2.0.1")
#configuration (TODO: build options menu and config file)
#number of images loaded for preview. (images not previewed will be shown as links)
maximages=10

import libzox
from libzox import pathfigure
from libzox import textitem
from libzox import progobj
from libzox import pathprogobj
from libzox import imgget
simplefont = pygame.font.SysFont("mono", 15)
hudfont = pygame.font.SysFont(None, 22)

bmlist=libzox.bmload()

#virtual desktop
class deskclass:
	def __init__(self, progs):
		self.progs=progs
		self.active=1
		#self.wallpaper=pygame.image.load("wallpaper.jpg")
		self.imgload=0
		self.clock=pygame.time.Clock()
		self.hovertext=""
		self.hoverprev=""
		return
	def process(self):
		
		while self.active:
			self.clock.tick(10)
			#yes i know its a bit of a wonky solution.
			for frame in framesc.proclist:
				if frame.ypos<69:
					frame.move(0, (frame.ypos-69))
					#frame.move(0, (-22))
		print("done.")
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==0:
			#status area routine. (works via routines setting deskt.hovertext on an active basis.
			if self.hovertext=="" and self.hovertext!=self.hoverprev:
				self.drawdesk(frameobj.surface)
				self.hoverprev=self.hovertext
				#print("clear")
			if self.hovertext!="" and self.hovertext!=self.hoverprev:
				self.drawdesk(frameobj.surface)
				self.hoverprev=self.hovertext
				#print("draw")
			self.hovertext=""
			
			for prog in self.progs:
				if prog.iconrect.collidepoint(pygame.mouse.get_pos()):
					self.hovertext=prog.hint
		#init code
		if frameobj.statflg==1:
			self.drawdesk(frameobj.surface)
		#shutdown code
		if frameobj.statflg==3:
			print("shutting down...")
			#prevent new connections.
			libgop.stopget=2
			self.active=0
		if frameobj.statflg==4:
			for prog in self.progs:
				if prog.iconrect.collidepoint(data.pos):
					framesc.add_frame(stz.framex(prog.xsize, prog.ysize, prog.friendly_name, pumpcall=prog.classref().pumpcall1, resizable=prog.resizable))
		#resize
		if frameobj.statflg==8:
			self.resize(frameobj.surface)
			self.drawdesk(frameobj.surface)#Needed only if a resizable desk is desired.
		if frameobj.statflg==6:
			mods=pygame.key.get_mods()
			for prog in self.progs:
				if prog.mod==None:
					if prog.key!=None:
						if data.key==prog.key:
							framesc.add_frame(stz.framex(prog.xsize, prog.ysize, prog.friendly_name, pumpcall=prog.classref().pumpcall1, resizable=prog.resizable))
				elif mods & prog.mod:
					if prog.key!=None:
						if data.key==prog.key:
							framesc.add_frame(stz.framex(prog.xsize, prog.ysize, prog.friendly_name, pumpcall=prog.classref().pumpcall1, resizable=prog.resizable))
			
	#resize handling
	def resize(self, surface):
		#self.wallpaperx=pygame.transform.scale(self.wallpaper, (surface.get_width(), surface.get_height()))
	##
		return
	def imageloader(self, surface):
		#self.wallpaper=pygame.image.load("wallpaper.jpg").convert(surface)
		self.mascot=pygame.image.load(os.path.join("vgop", "mascot45.png"))
		self.resize(surface)
		for prog in self.progs:
			prog.icon=prog.icon.convert(surface)
	##
	def drawdesk(self, surface):
		if not self.imgload:
			self.imgload=1
			self.imageloader(surface)
			
		#surface.blit(self.wallpaperx, (0, 0))
		#surface.blit(self.mascot, (surface.get_width()//2-self.mascot.get_width()//2, surface.get_height()//2-self.mascot.get_height()//2))
		icnx=0
		icny=0
		icnxjmp=45
		icnyjmp=50
		pygame.draw.rect(surface, (60, 60, 120), pygame.Rect(0, 0, surface.get_width(), 45))
		for prog in self.progs:
			prog.iconrect=surface.blit(prog.icon, (icnx, icny))
			icnx+=icnxjmp
			
		#urllabel=simplefont.render(self.hovertext, True, (255, 255, 255), (60, 60, 120))
		urllabel=hudfont.render(self.hovertext, True, (255, 255, 255), (60, 60, 120))
		surface.blit(urllabel, (icnx+10, 10))
		surface.blit(self.mascot, (surface.get_width()-self.mascot.get_width(), 0))







#text document wrapper for gopherpane
def textshow(host, port, selector):
	data=pathfigure(host, port, selector, gtype="0")
	menu=libgop.menudecode(data, txtflg=1)
	newgop=gopherpane(host=host, port=port, selector=selector, preload=menu, prefix="text: gopher://", gtype="0", shortprefix="text: ")
	framesc.add_frame(stz.framex(600, 500, "Text Document", resizable=1, pumpcall=newgop.pumpcall1, xpos=20))



#gopher menu class. also used for text documents
class gopherpane:
	def __init__(self, host='about:splash', port=70, selector="", prefix="menu: gopher://", preload=None, forceimage=0, linkdisable=0, gtype="1", shortprefix="menu: "):
		self.host=host
		self.port=port
		self.selector=selector
		self.yoff=0
		self.yjump=15
		self.menu=[]
		self.data=None
		self.prefix=prefix
		self.preload=preload
		self.forceimage=forceimage
		self.linkdisable=linkdisable
		self.renderdict={}
		self.gtype=gtype
		self.shortprefix=shortprefix
	#menu get routine
	def menuget(self):
		self.data=pathfigure(self.host, self.port, self.selector)
		self.menu=libgop.menudecode(self.data)
		for item in self.renderdict:
			del item
		del self.renderdict
		self.renderdict={}
	#render routine
	def menudraw(self, frameobj):
		imageset=[]
		imagecount=0
		self.ypos=self.yoff
		frameobj.surface.fill((255, 255, 255))
		
		for item in self.menu:
			if item.gtype=="i" or item.gtype==None:
				rects, self.ypos, self.renderdict = textitem(item.name, simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.ypos, self.renderdict)
			elif item.gtype=="1":
				rect, self.ypos, self.renderdict = textitem("[MENU]" + item.name, simplefont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict)
				item.rect=rect
			elif item.gtype=="7":
				rect, self.ypos, self.renderdict = textitem("[QUERY]" + item.name, simplefont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict)
				item.rect=rect
			elif item.gtype=="0":
				rect, self.ypos, self.renderdict = textitem("[TEXT]" + item.name, simplefont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict)
				item.rect=rect
			#image preview routine
			elif item.gtype=="g" or item.gtype=="p" or item.gtype=="I":
				imagecount+=1
				try:
					if item.image!=None:
						item.rect=frameobj.surface.blit(item.image, (0, self.ypos))
						self.ypos+=item.image.get_height()
					if item.image==None:
						item.rect, self.ypos, self.renderdict = textitem("[IMAGE]" + item.name, simplefont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict)
					#pygame.draw.rect(frameobj.surface, (255, 255, 0), item.rect, 1)
				except AttributeError as err:
					#print(err)
					item.image=None
					if imagecount<maximages or (imagecount<2 and self.forceimage):
						imageset.extend([item])
					item.rect, self.ypos, self.renderdict = textitem("[IMAGE]" + item.name, simplefont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict)

					
						
				
					
			else:
				rects, self.ypos, self.renderdict = textitem("[UNKNOWN:" + item.gtype + "]" + item.name, simplefont, 15, (0, 0, 0), frameobj.surface, self.ypos, self.renderdict)
				#print(item.gtype)
		#launch image loader thread if needed
		if imageset!=[]:
			sideproc=Thread(target = imgget, args = [imageset, self.menudraw, frameobj])
			sideproc.daemon=True
			sideproc.start()
	#menu change loader
	def menuchange(self, item, frameobj):
		self.host=item.hostname
		self.port=item.port
		self.selector=item.selector
		if item.hostname.startswith("about:"):
			frameobj.name=(self.shortprefix+str(item.hostname))
		else:
			frameobj.name=(self.prefix+str(item.hostname) + "/" + self.gtype + str(item.selector))
		self.menuget()
		self.yoff=0
		self.menudraw(frameobj)
		return
	#menu initalization loader
	def menuinital(self, frameobj):
		if self.host.startswith("about:"):
			frameobj.name=(self.shortprefix+str(self.host))
		else:
			frameobj.name=(self.prefix+str(self.host) + "/" + self.gtype + str(self.selector))
		self.menuget()
		self.yoff=0
		self.menudraw(frameobj)
	def pumpcall1(self, frameobj, data=None):
		
		#link destination preview routine. 
		if frameobj.statflg==0 and frameobj.wo==0:
			for item in self.menu:
				if item.gtype!=None:
					if item.gtype in "01pgI7":
						try:
							if item.rect.collidepoint(stz.mousehelper(pygame.mouse.get_pos(), frameobj)):
								if item.hostname.startswith("about:"):
									deskt.hovertext=(item.hostname)
								else:
									deskt.hovertext=("gopher://" + item.hostname + "/" + item.gtype + item.selector)
								break
						except AttributeError:
							continue
		#delete some of the larger things upon close
		if frameobj.statflg==3:
			for item in self.renderdict:
				del item
			del self.renderdict
			del self.menu
			del self.data
		#startup
		if frameobj.statflg==1:
			if self.preload==None:
				sideproc=Thread(target = self.menuinital, args = [frameobj])
				sideproc.daemon=True
				sideproc.start()
			else:
				self.menu=self.preload
				self.menudraw(frameobj)
				if self.host.startswith("about:"):
					frameobj.name=(self.shortprefix+str(self.host))
				else:
					frameobj.name=(self.prefix+str(self.host) + "/" + self.gtype + str(self.selector))
		#resize
		if frameobj.statflg==2:
			self.yoff=0
			for item in self.renderdict:
				del item
			del self.renderdict
			self.renderdict={}
			self.menudraw(frameobj)
		#mouse button down
		if frameobj.statflg==6:
			if data.key==pygame.K_UP:
				self.yoff+=self.yjump*2
				if self.yoff>0:
					self.yoff=0
				self.menudraw(frameobj)
			if data.key==pygame.K_DOWN and self.ypos>frameobj.sizey:
				self.yoff-=self.yjump*2
				self.menudraw(frameobj)
			if data.key==pygame.K_m:
				newgop=bookmadded(url=libzox.gurlencode(self.host, self.selector, self.gtype, self.port))
				framesc.add_frame(stz.framex(350, 100, "New Bookmark", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50))
				

		if frameobj.statflg==4:
			if data.button==1 and not self.linkdisable:
				for item in self.menu:
					mods=pygame.key.get_mods()
					
					if mods & pygame.KMOD_SHIFT:
						if item.gtype!=None:
							if item.gtype in "10gpI7":
								if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
									newgop=bookmadded(url=libzox.gurlencode(item.hostname, item.selector, item.gtype, item.port))
									framesc.add_frame(stz.framex(350, 100, "New Bookmark", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50))

					else:
						
						if item.gtype=="1":
							if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
								self.menu=[]
								sideproc=Thread(target = self.menuchange, args = [item, frameobj])
								sideproc.daemon=True
								sideproc.start()
								break
						if item.gtype=="0":
							if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
								sideproc=Thread(target = textshow, args = [item.hostname, item.port, item.selector])
								sideproc.daemon=True
								sideproc.start()
								break
						if item.gtype=="g" or item.gtype=="p" or item.gtype=="I":
							if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
								#itemcopy=copy.deepcopy(item)
								#del itemcopy.image
								#newgop=gopherpane(host=itemcopy.hostname, port=itemcopy.port, selector=itemcopy.selector, prefix="image: gopher://", preload=[itemcopy], forceimage=1, linkdisable=1, gtype=item.gtype, shortprefix="image: ")
								newgop=imgview(host=item.hostname, port=item.port, selector=item.selector, gtype=item.gtype, imagesurf=item.image)
								framesc.add_frame(stz.framex(500, 400, "Image", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50))
						if item.gtype=="7":
							if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
								newgop=querypane(host=item.hostname, port=item.port, selector=item.selector)
								framesc.add_frame(stz.framex(350, 100, "Gopher Query", resizable=0, pumpcall=newgop.pumpcall1))
			if data.button==3 and not self.linkdisable:
				for item in self.menu:
					if item.gtype=="1":
						if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
							newgop=gopherpane(host=item.hostname, port=item.port, selector=item.selector)
							framesc.add_frame(stz.framex(600, 500, "Gopher Menu", resizable=1, pumpcall=newgop.pumpcall1))
			if data.button==4:
				self.yoff+=self.yjump*2
				if self.yoff>0:
					self.yoff=0
				self.menudraw(frameobj)
			if data.button==5 and self.ypos>frameobj.sizey:
				self.yoff-=self.yjump*2
				self.menudraw(frameobj)
							
					
		return
			

#query (gopher item type 7) dialog box
class querypane:
	def __init__(self, host, port, selector):
		self.host=host
		self.port=port
		self.selector=selector
		self.yoff=0
		#self.hovmsg="Enter your query into the serarch box"
		self.yjump=15
		self.stringblob=""
		if self.host=="QUERYTEST":
			self.debug=1
		else:
			self.debug=0
		self.validchars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890"
	def renderdisp(self, frameobj):
		str1=self.host+"/7"+self.selector
		frameobj.surface.fill((255, 255, 255))
		textitem(str1, simplefont, self.yjump, (0, 0, 0), frameobj.surface, 0, {})
		textitem("Please Type Query", simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.yjump*2, {})
		textitem(">"+self.stringblob+"|", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*4, {})
	def loader(self, frameobj):
		frameobj.name="Loading..."
		try:
			data=libgop.gopherget(self.host, self.port, self.selector, query=self.stringblob)
		except Exception as err:
			print(err)
			data=open(os.path.join("vgop", "gaierror"))
		menu=libgop.menudecode(data)
		newgop=gopherpane(host=self.host, port=self.port, selector=self.selector, preload=menu)
		framesc.add_frame(stz.framex(600, 500, "Gopher Menu", resizable=1, pumpcall=newgop.pumpcall1))
		#close self
		framesc.close_pid(frameobj.pid)
	def pumpcall1(self, frameobj, data=None):
		#if frameobj.statflg==0:
			#show hint in hover text area
			#if frameobj.wo==0:
			#	deskt.hovertext=self.hovmsg
		if frameobj.statflg==2:
			self.renderdisp(frameobj)
		if frameobj.statflg==1:
			str1=self.host+"/7"+self.selector
			print("querypane:")
			print(str1)
			frameobj.name="query: "+str1
			self.renderdisp(frameobj)
		#if frameobj.statflg==3:
		#	if deskt.hovertext==self.hovmsg:
		#		deskt.hovertext=""
		if frameobj.statflg==6:
			if data.key==pygame.K_RETURN:
				if self.debug==1:
					print(self.stringblob)
				else:
					sideproc=Thread(target = self.loader, args = [frameobj])
					sideproc.daemon=True
					sideproc.start()
			elif data.key==pygame.K_BACKSPACE:
				self.stringblob=self.stringblob[:-1]
				#print(self.stringblob)
				self.renderdisp(frameobj)
			else:
				if str(data.unicode) in self.validchars:
					self.stringblob+=str(data.unicode)
					#print(self.stringblob)
					self.renderdisp(frameobj)
				
		

#bookmark creator/editor dialog.
class bookmarks:
	def __init__(self, url="", bookm=None):
		self.yoff=0
		self.yjump=15
		self.stringblob=""
		#self.hovmsg="Enter a gopher URL to load."
		self.validchars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890:/.-_ "
		#self.url=url
		self.bookm=bookm
		self.url=url
		#self.mode=mode
		self.renderdict={}
		self.urlblob=url
		self.nameblob=""
		if self.bookm!=None:
			self.urlblob=self.bookm.url
			self.nameblob=self.bookm.name
		self.del0=pygame.image.load(os.path.join("vgop", "delinact.png")).convert()
		self.del1=pygame.image.load(os.path.join("vgop", "delact.png")).convert()
		self.go0=pygame.image.load(os.path.join("vgop", "goinact.png")).convert()
		self.go1=pygame.image.load(os.path.join("vgop", "goact.png")).convert()
		self.edit0=pygame.image.load(os.path.join("vgop", "editinact.png")).convert()
		self.edit1=pygame.image.load(os.path.join("vgop", "editact.png")).convert()
		self.newbm=pygame.image.load(os.path.join("vgop", "newbm.png")).convert()
		self.funct=0
		self.bmprev=None
		self.offset=0
	def loaderg1(self, frameobj):
		try:
			data=pathfigure(self.host, self.port, self.selector)
		except Exception:
			data=open(os.path.join("vgop", "gaierror"))
		menu=libgop.menudecode(data)
		newgop=gopherpane(host=self.host, port=self.port, selector=self.selector, preload=menu)
		framesc.add_frame(stz.framex(600, 500, "Gopher Menu", resizable=1, pumpcall=newgop.pumpcall1))
		#close self
		self.offset=0
	def loaderg0(self, frameobj):
		textshow(self.host, self.port, self.selector)
	def renderdisp(self, frameobj):
		if self.offset>0:
			xlist=bmlist[self.offset:]
		else:
			xlist=bmlist
		frameobj.surface.fill((255, 255, 255))
		self.newrect=frameobj.surface.blit(self.newbm, (150, 0))
		if self.funct==0:
			self.gorect=frameobj.surface.blit(self.go1, (0, 0))
			self.delrect=frameobj.surface.blit(self.del0, (50, 0))
			self.editrect=frameobj.surface.blit(self.edit0, (100, 0))
		elif self.funct==1:
			self.gorect=frameobj.surface.blit(self.go0, (0, 0))
			self.delrect=frameobj.surface.blit(self.del1, (50, 0))
			self.editrect=frameobj.surface.blit(self.edit0, (100, 0))
		else:
			self.gorect=frameobj.surface.blit(self.go0, (0, 0))
			self.delrect=frameobj.surface.blit(self.del0, (50, 0))
			self.editrect=frameobj.surface.blit(self.edit1, (100, 0))
		self.ypos=40
		for item in xlist:
			item.rect, self.ypos, self.renderdict = textitem(item.name, simplefont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict)
	
	def rotarylaunch(self, url, frameobj):
		self.host, self.port, self.selector, self.gtype = libzox.gurldecode(url)
		if self.gtype=="1":
			sideproc=Thread(target = self.loaderg1, args = [frameobj])
			sideproc.daemon=True
			sideproc.start()
		elif self.gtype=="0":
			sideproc=Thread(target = self.loaderg0, args = [frameobj])
			sideproc.daemon=True
			sideproc.start()
		elif self.gtype=="7":
			newgop=querypane(host=self.host, port=self.port, selector=self.selector)
			framesc.add_frame(stz.framex(350, 100, "Gopher Query", resizable=0, pumpcall=newgop.pumpcall1))
		elif self.gtype=="g" or self.gtype=="p" or self.gtype=="I":
			newgop=imgview(host=self.host, port=self.port, selector=self.selector, gtype=self.gtype)
			framesc.add_frame(stz.framex(500, 400, "Image", resizable=1, pumpcall=newgop.pumpcall1))
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==0 and self.bmprev!=bmlist:
			self.bmprev=list(bmlist)
			self.offset=0
			self.renderdisp(frameobj)
		if frameobj.statflg==1:
			frameobj.name="Bookmarks"
			self.renderdisp(frameobj)
		if frameobj.statflg==4:
			if data.button==4:
				self.offset-=1
				if self.offset<0:
					self.offset==0
				self.renderdisp(frameobj)
			if data.button==5:
				self.offset+=1
				if self.offset>len(bmlist)-1 and len(bmlist)>0:
					self.offset=len(bmlist)-1
				self.renderdisp(frameobj)
			if data.button==1:
				if self.newrect.collidepoint(stz.mousehelper(data.pos, frameobj)):
					newgop=bookmadded()
					framesc.add_frame(stz.framex(350, 100, "New Bookmark", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50))
				if self.editrect.collidepoint(stz.mousehelper(data.pos, frameobj)):
					self.funct=2
					self.renderdisp(frameobj)
				if self.delrect.collidepoint(stz.mousehelper(data.pos, frameobj)):
					self.funct=1
					self.renderdisp(frameobj)
				if self.gorect.collidepoint(stz.mousehelper(data.pos, frameobj)):
					self.funct=0
					self.renderdisp(frameobj)
				
				for item in bmlist:
					if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
						if self.funct==0:
							self.rotarylaunch(item.url, frameobj)
						if self.funct==1:
							newgop=bookdel(item)
							framesc.add_frame(stz.framex(350, 100, "Please Confirm:", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50))
						if self.funct==2:
							newgop=bookmadded(bookm=item)
							framesc.add_frame(stz.framex(350, 100, "Edit Bookmark", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50))
		



#bookmark creator/editor dialog.
class bookmadded:
	def __init__(self, url="", bookm=None):
		self.yoff=0
		self.yjump=15
		self.stringblob=""
		#self.hovmsg="Enter a gopher URL to load."
		self.validchars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890:/.-_ "
		#self.url=url
		self.bookm=bookm
		self.url=url
		#self.mode=mode
		self.urlblob=url
		self.nameblob=""
		if self.bookm!=None:
			self.urlblob=self.bookm.url
			self.nameblob=self.bookm.name
		self.line=1
	def renderdisp(self, frameobj):
		frameobj.surface.fill((255, 255, 255))
		textitem("tab=switch entries, enter=accept", simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.yjump*1, {})
		if self.line:
			textitem("gopher://"+self.urlblob+"", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*3, {})
			textitem("name:"+self.nameblob+"|", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*5, {})
		else:
			textitem("gopher://"+self.urlblob+"|", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*3, {})
			textitem("name:"+self.nameblob+"", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*5, {})
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==2:
			self.renderdisp(frameobj)
		if frameobj.statflg==1:
			if self.bookm==None:
				frameobj.name="New Bookmark: " + self.url
			else:
				frameobj.name="Edit Bookmark: "
			self.renderdisp(frameobj)
		if frameobj.statflg==6:
			if data.key==pygame.K_RETURN and self.nameblob.replace(" ", "")!="":
				if self.bookm==None:
					newbook=libzox.bmitem(self.urlblob, self.nameblob)
					bmlist.extend([newbook])
					libzox.bmsave(bmlist)
				else:
					self.bookm.name=self.nameblob
					self.bookm.url=self.urlblob
					libzox.bmsave(bmlist)
				framesc.close_pid(frameobj.pid)
			elif data.key==pygame.K_BACKSPACE:
				if self.line:
					self.nameblob=self.nameblob[:-1]
				else:
					self.urlblob=self.urlblob[:-1]
				#print(self.stringblob)
				self.renderdisp(frameobj)
			elif data.key==pygame.K_TAB:
				if self.line:
					self.line=0
				else:
					self.line=1
				self.renderdisp(frameobj)
			else:
				if str(data.unicode) in self.validchars:
					if self.line:
						self.nameblob+=str(data.unicode)
					else:
						self.urlblob+=str(data.unicode)
					#print(self.stringblob)
					self.renderdisp(frameobj)


class bookdel:
	def __init__(self, bookm):
		self.yoff=0
		self.yjump=15
		self.bookm=bookm
		self.urlblob=self.bookm.url
		self.nameblob=self.bookm.name
	def renderdisp(self, frameobj):
		frameobj.surface.fill((255, 255, 255))
		textitem("Delete Bookmark? [Y]es or [N]o.", simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.yjump*1, {})
		textitem("gopher://"+self.urlblob, simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*3, {})
		textitem("name:"+self.nameblob, simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*5, {})
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==2:
			self.renderdisp(frameobj)
		if frameobj.statflg==1:
			frameobj.name="Please Confirm:"
			self.renderdisp(frameobj)
		if frameobj.statflg==6:
			if data.key==pygame.K_y:
				bmlist.remove(self.bookm)
				libzox.bmsave(bmlist)
				framesc.close_pid(frameobj.pid)
			elif data.key==pygame.K_n:
				framesc.close_pid(frameobj.pid)
				

#url entry dialog box.
class urlgo:
	def __init__(self):
		self.yoff=0
		self.yjump=15
		self.stringblob=""
		#self.hovmsg="Enter a gopher URL to load."
		self.validchars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890:/.-_"
	def renderdisp(self, frameobj):
		frameobj.surface.fill((255, 255, 255))
		textitem("Please Type URL", simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.yjump*2, {})
		textitem("gopher://"+self.stringblob+"|", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*4, {})
	def loaderg1(self, frameobj):
		frameobj.name="Loading: gopher://"+self.stringblob+" ..." 
		try:
			data=pathfigure(self.host, self.port, self.selector)
		except Exception:
			data=open(os.path.join("vgop", "gaierror"))
		menu=libgop.menudecode(data)
		newgop=gopherpane(host=self.host, port=self.port, selector=self.selector, preload=menu)
		framesc.add_frame(stz.framex(600, 500, "Gopher Menu", resizable=1, pumpcall=newgop.pumpcall1))
		#close self
		framesc.close_pid(frameobj.pid)
	def loaderg0(self, frameobj):
		textshow(self.host, self.port, self.selector)
		framesc.close_pid(frameobj.pid)
	def pumpcall1(self, frameobj, data=None):
		#if frameobj.statflg==0:
		#	#show hint in hover text area
		#	if frameobj.wo==0:
		#		deskt.hovertext=self.hovmsg
		#if frameobj.statflg==3:
		#	if deskt.hovertext==self.hovmsg:
		#		deskt.hovertext=""
		if frameobj.statflg==2:
			self.renderdisp(frameobj)
		if frameobj.statflg==1:
			
			frameobj.name="URL GO:"
			self.renderdisp(frameobj)
		if frameobj.statflg==6:
			if data.key==pygame.K_RETURN:
				try:
					
					if self.stringblob.startswith("about:"):
						self.host=self.stringblob
						self.port=70
						self.selector=""
						#self.gtype="1"
						if "/" in self.stringblob:
							self.host, self.selecttype = self.stringblob.split("/", 1)
							self.gtype=self.selecttype[0]
						else:
							self.gtype="1"
					else:
						
						if ":" in self.stringblob:
							self.port=self.stringblob.split(":")[1]
							self.stringblob=self.stringblob.split(":")[0]
						else:
							self.port=70
						if "/" in self.stringblob:
							self.host, self.selecttype = self.stringblob.split("/", 1)
							self.gtype=self.selecttype[0]
							self.selector=self.selecttype[1:]
						else:
							self.host=self.stringblob
							self.gtype="1"
							self.selector="/"
							
					if self.gtype=="1":
						sideproc=Thread(target = self.loaderg1, args = [frameobj])
						sideproc.daemon=True
						sideproc.start()
					elif self.gtype=="0":
						sideproc=Thread(target = self.loaderg0, args = [frameobj])
						sideproc.daemon=True
						sideproc.start()
					elif self.gtype=="7":
						newgop=querypane(host=self.host, port=self.port, selector=self.selector)
						framesc.add_frame(stz.framex(350, 100, "Gopher Query", resizable=0, pumpcall=newgop.pumpcall1))
						framesc.close_pid(frameobj.pid)
					elif self.gtype=="g" or self.gtype=="p" or self.gtype=="I":
						newgop=imgview(host=self.host, port=self.port, selector=self.selector, gtype=self.gtype)
						framesc.add_frame(stz.framex(500, 400, "Image", resizable=1, pumpcall=newgop.pumpcall1))
						framesc.close_pid(frameobj.pid)
				except IndexError as err:
					print(err)
			elif data.key==pygame.K_BACKSPACE:
				self.stringblob=self.stringblob[:-1]
				#print(self.stringblob)
				self.renderdisp(frameobj)
			else:
				if str(data.unicode) in self.validchars:
					self.stringblob+=str(data.unicode)
					#print(self.stringblob)
					self.renderdisp(frameobj)
				

#image viewer
class imgview:
	def __init__(self, host, port, selector, gtype="I", imagesurf=None):
		self.host=host
		self.port=port
		self.selector=selector
		self.gtype=gtype
		self.imagesurf=imagesurf
		self.pscf=None
		self.pan=0
		self.loaderupt=0
		self.dummysurf=pygame.image.load(os.path.join("vgop", "loadingimage.png"))
		if self.imagesurf==None:
			self.surf=self.dummysurf
			sideproc=Thread(target = self.imageload)
			sideproc.daemon=True
			sideproc.start()
		else:
			self.surf=self.imagesurf
	def imageload(self):
		data=pathfigure(self.host, self.port, self.selector, gtype=self.gtype)
		try:
			if self.gtype=="g":
				imagefx=pygame.image.load(data, "quack.gif")
			if self.gtype=="p":
				imagefx=pygame.image.load(data, "quack.png")
			if self.gtype=="I":
				imagefx=pygame.image.load(data)
			imagefx.convert()
			self.surf=imagefx
		except pygame.error:
			self.surf=pygame.image.load(os.path.join("vgop", "giaerror.png"))
			print("imgview: Failed to load.")
		self.loaderupt=1
		
	def updatedisp(self, frameobj):
		if self.pscf!=self.scf:
			self.surftran=pygame.transform.scale(self.surf, ((int(self.imgx * self.scf)), (int(self.imgy * self.scf))))
			self.pscf=self.scf
		self.imgbox = self.surftran.get_rect()
		self.imgbox.centerx = self.xoff
		self.imgbox.centery = self.yoff
		frameobj.surface.fill((255, 255, 255))
		frameobj.surface.blit(self.surftran, self.imgbox)
	def pumpcall1(self, frameobj, data=None):
		
		if frameobj.statflg==0 and self.pan:
			self.mpos=pygame.mouse.get_pos()
			
			self.xoff+=(self.mpos[0]-self.ppos[0])
			self.yoff+=(self.mpos[1]-self.ppos[1])
			self.ppos=self.mpos
			self.updatedisp(frameobj)
			
		if frameobj.statflg==1:
			if self.host.startswith("about:"):
				frameobj.name=("Image: " + str(self.host) + "/" + self.gtype)
			else:
				frameobj.name=("Image: gopher://" + self.host + "/" + self.gtype + self.selector)
		if frameobj.statflg==1 or frameobj.statflg==2 or self.loaderupt:
			
			self.pscf=None
			self.loaderupt=0
			self.surfx=frameobj.sizex
			self.surfy=frameobj.sizey
			self.imgx=self.surf.get_width()
			self.imgy=self.surf.get_height()
			scfx=(float(self.surfx) / self.imgx)
			scfy=(self.surfy) / float(self.imgy)
			self.xoff=self.surfx//2
			self.yoff=self.surfy//2
			if scfx>scfy:
				scf=scfy
			else:
				scf=scfx
			
			self.scfdef=scf
			self.scf=scf
			self.updatedisp(frameobj)
		if frameobj.statflg==4:
			if data.button==5:
				self.scf-=0.3
				if self.scf<0.1:
					self.scf=0.1
			if data.button==4:
				self.scf+=0.3
			if data.button==1:
				self.ppos=data.pos
				self.pan=1
			if data.button==3:
				self.xoff=self.surfx//2
				self.yoff=self.surfy//2
				self.scf=self.scfdef
				self.updatedisp(frameobj)
		if frameobj.statflg==5:
			if data.button==1:
				self.pan=0
			self.updatedisp(frameobj)
		if frameobj.statflg==6:
			if data.key==pygame.K_m:
				newgop=bookmadded(url=libzox.gurlencode(self.host, self.selector, self.gtype, self.port))
				framesc.add_frame(stz.framex(350, 100, "New Bookmark", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50))

		return


#desktop icons
progs=[progobj(gopherpane, pygame.image.load(os.path.join("vgop", "newwindow.png")), "goppane", "Gopher Menu", "GOPHER", 600, 500, 1, key=pygame.K_n, mod=pygame.KMOD_CTRL, hint="Open a new gopher window (CTRL+n)"),
progobj(urlgo, pygame.image.load(os.path.join("vgop", "go.png")), "urlgo", "URL GO:", "urlgo", 400, 100, 0, key=pygame.K_g, mod=pygame.KMOD_CTRL, hint="Enter a Gopher URL to load. (CTRL+g)"),
progobj(bookmarks, pygame.image.load(os.path.join("vgop", "bookmarks.png")), "bookmarks", "Bookmarks", "bookmarks", 600, 500, 1, key=pygame.K_b, mod=pygame.KMOD_CTRL, hint="Open bookmarks (CTRL+b)"),

pathprogobj(gopherpane, pygame.image.load(os.path.join("vgop", "help.png")), "goppane_HELP", "Gopher Menu", "GOPHER_HELP", 600, 500, 1, host="about:help", key=pygame.K_F1, hint="Bring up a help menu. (F1)")]
deskt=deskclass(progs)
pygame.font.init()


#logical equivalent to the desktop's "frame"
deskframe=stz.desktop(800, 600, "Zoxenpher", pumpcall=deskt.pumpcall1, resizable=1)

windowicon=pygame.image.load(os.path.join("vgop", "icon32.png"))
framesc=stz.framescape(deskframe, deskicon=windowicon)

#start auxilary desktop thread.
sideproc=Thread(target = deskt.process, args = [])
sideproc.start()


#start wm (takes over main thread)
framesc.process()




