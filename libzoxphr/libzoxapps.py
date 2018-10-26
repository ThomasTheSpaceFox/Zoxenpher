#!/usr/bin/env python
#import time
import os
import sys
import libgop
import pygame
from threading import Thread
from . import strazoloidwm as stz
from . import libzox
from .libzox import pathfigure
from .libzox import textitem
from .libzox import imgget
import subprocess
from subprocess import Popen
from . import libzoxui

simplefont = pygame.font.SysFont(libzox.cnfdict["menufont"], int(libzox.cnfdict["menufontsize"]))
linkfont = pygame.font.SysFont(libzox.cnfdict["menufont"], int(libzox.cnfdict["menufontsize"]))
linkfont.set_underline(1)
tilestr=libzox.cnfdict["bgtile"]
if tilestr=="none":
	tiledraw=None
else:
	try:
		tiledraw=pygame.image.load(os.path.join("vgop", tilestr))
	except pygame.error:
		try:
			tiledraw=pygame.image.load(os.path.join("usr", tilestr))
		except pygame.error:
			tiledraw=None

histsize=int(libzox.cnfdict["histsize"])


gopherwidth=((simplefont.size("_")[0])*81)+25

gfontjump=int(libzox.cnfdict["menutextjump"])

gopherheight=int(libzox.cnfdict["menuheight"])

hudfont = pygame.font.SysFont(None, 22)
pygame.mixer.init()
maximages=int(libzox.cnfdict["imgpreview"])
bmlist=libzox.bmload()
#menu window graphics
bookbtn=pygame.image.load(os.path.join("vgop", "bookbtn.png"))
menucorner=pygame.image.load(os.path.join("vgop", "menucorner.png"))
menucorner_wait=pygame.image.load(os.path.join("vgop", "menucorner_wait.png"))
loadbtn=pygame.image.load(os.path.join("vgop", "loadbtn.png"))
loadbtn_inact=pygame.image.load(os.path.join("vgop", "loadbtn_inact.png"))

backbtn=pygame.image.load(os.path.join("vgop", "backbtn.png"))
backbtn_inact=pygame.image.load(os.path.join("vgop", "backbtn_inact.png"))
nextbtn=pygame.image.load(os.path.join("vgop", "nextbtn.png"))
nextbtn_inact=pygame.image.load(os.path.join("vgop", "nextbtn_inact.png"))
upbtn=pygame.image.load(os.path.join("vgop", "upbtn.png"))
upbtn_inact=pygame.image.load(os.path.join("vgop", "upbtn_inact.png"))
rootbtn=pygame.image.load(os.path.join("vgop", "rootbtn.png"))
rootbtn_inact=pygame.image.load(os.path.join("vgop", "rootbtn_inact.png"))

#common:
scrollup=pygame.image.load(os.path.join("vgop", "scrollu.png"))
scrolldn=pygame.image.load(os.path.join("vgop", "scrolld.png"))
scrollup_no=pygame.image.load(os.path.join("vgop", "scrollu_no.png"))
scrolldn_no=pygame.image.load(os.path.join("vgop", "scrolld_no.png"))

#bookmark window graphics
bookm_del0=pygame.image.load(os.path.join("vgop", "delinact.png"))
bookm_del1=pygame.image.load(os.path.join("vgop", "delact.png"))
bookm_go0=pygame.image.load(os.path.join("vgop", "goinact.png"))
bookm_go1=pygame.image.load(os.path.join("vgop", "goact.png"))
bookm_edit0=pygame.image.load(os.path.join("vgop", "editinact.png"))
bookm_edit1=pygame.image.load(os.path.join("vgop", "editact.png"))
bookm_newbm=pygame.image.load(os.path.join("vgop", "newbm.png"))
menucorner_book=pygame.image.load(os.path.join("vgop", "menucorner_book.png"))




framesc=None

def init(framescape, desktop):
	global framesc
	global gtmenu
	global gtmenuremote
	global gtmenuint
	global gtmenuroot
	
	global gtimage
	global gttext
	global gtquery
	
	global gtsound
	global gtbin
	global gtweb
	global gterror
	
	global deskt
	deskt=desktop
	framesc=framescape
	#load Gopher type icons.
	gtmenu=pygame.image.load(os.path.join("vgop", "menuicn.png")).convert()
	gtmenuremote=pygame.image.load(os.path.join("vgop", "menuremoteicn.png")).convert()
	gtmenuint=pygame.image.load(os.path.join("vgop", "menuinticn.png")).convert()
	gtmenuroot=pygame.image.load(os.path.join("vgop", "menurooticn.png")).convert()
	
	gtimage=pygame.image.load(os.path.join("vgop", "imageicon.png")).convert()
	gttext=pygame.image.load(os.path.join("vgop", "texticon.png")).convert()
	gtquery=pygame.image.load(os.path.join("vgop", "queryicon.png")).convert()
	
	gtsound=pygame.image.load(os.path.join("vgop", "soundicn.png")).convert()
	gtbin=pygame.image.load(os.path.join("vgop", "binicn.png")).convert()
	gtweb=pygame.image.load(os.path.join("vgop", "webicn.png")).convert()
	gterror=pygame.image.load(os.path.join("vgop", "erroricn.png")).convert()






#
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
		self.mattesurf=None
		return
	#def process(self):
	#	while self.active:
	#		self.clock.tick(1)
	#	print("done.")
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
			mpos=pygame.mouse.get_pos()
			for prog in self.progs:
				if prog.iconrect.collidepoint(mpos):
					self.hovertext=prog.hint
			
			if self.mascotrect.collidepoint(mpos):
				self.hovertext="About Zoxenpher."
		#init code
		if frameobj.statflg==1:
			stz.setminy(46)
			self.drawdesk(frameobj.surface)
		#shutdown code
		if frameobj.statflg==3:
			print("shutting down...")
			#prevent new connections.
			libgop.stopget=2
			self.active=0
		if frameobj.statflg==4:
			if self.mascotrect.collidepoint(data.pos):
				newgop=gopherpane(host="about:about", port=70, selector="/", shortprefix="About: ")
				framesc.add_frame(stz.framex(gopherwidth, gopherheight, "Gopher Menu", resizable=1, pumpcall=newgop.pumpcall1))
			for prog in self.progs:
				if prog.iconrect.collidepoint(data.pos):
					framesc.add_frame(stz.framex(prog.xsize, prog.ysize, prog.friendly_name, pumpcall=prog.classref().pumpcall1, resizable=prog.resizable))
		#resize
		if frameobj.statflg==8:
			self.resize(frameobj.surface)
			#reset tile background
			self.mattesurf=None
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
		self.mascot=pygame.image.load(os.path.join("vgop", "mascot45.png")).convert(surface)
		self.iconend=pygame.image.load(os.path.join("vgop", "iconbarend.png")).convert(surface)
		self.iconbegin=pygame.image.load(os.path.join("vgop", "iconbarbegin.png")).convert(surface)
		self.resize(surface)
		if tiledraw!=None:
			self.tilesurf=tiledraw.convert(surface)
		else:
			self.tilesurf=None
		for prog in self.progs:
			prog.icon=prog.icon.convert(surface)
	##
	def drawdesk(self, surface):
		if not self.imgload:
			self.imgload=1
			self.imageloader(surface)
			
		if self.tilesurf!=None:
			if self.mattesurf==None:
				self.mattesurf=(libzox.tiledraw(surface, self.tilesurf)).convert(surface)
			surface.blit(self.mattesurf, (0, 0))
			
			
			
		#surface.blit(self.wallpaperx, (0, 0))
		#surface.blit(self.mascot, (surface.get_width()//2-self.mascot.get_width()//2, surface.get_height()//2-self.mascot.get_height()//2))
		icnx=0
		icny=0
		icnxjmp=45
		icnyjmp=50
		pygame.draw.rect(surface, (60, 60, 120), pygame.Rect(0, 0, surface.get_width(), 45))
		pygame.draw.line(surface, (20, 40, 80), (0, 45), (surface.get_width(), 45), 1)
		for prog in self.progs:
			if not prog.side:
				prog.iconrect=surface.blit(prog.icon, (icnx, icny))
				icnx+=icnxjmp
		surface.blit(self.iconend, (icnx, icny))
		icnx+=icnxjmp//2
		
		#urllabel=simplefont.render(self.hovertext, True, (255, 255, 255), (60, 60, 120))
		urllabel=hudfont.render(self.hovertext, True, (255, 255, 255), (60, 60, 120))
		surface.blit(urllabel, (icnx+10, 10))
		mascotx=surface.get_width()-self.mascot.get_width()
		self.mascotrect=surface.blit(self.mascot, (mascotx, 0))
		for prog in self.progs:
			if prog.side:
				mascotx-=45
				prog.iconrect=surface.blit(prog.icon, (mascotx, icny))
		surface.blit(self.iconbegin, (mascotx-self.iconbegin.get_width(), 0))







#text document wrapper for gopherpane
def textshow(host, port, selector):
	data=pathfigure(host, port, selector, gtype="0")
	menu=libgop.menudecode(data, txtflg=1)
	newgop=gopherpane(host=host, port=port, selector=selector, preload=menu, prefix="text: gopher://", gtype="0", shortprefix="text: ")
	framesc.add_frame(stz.framex(gopherwidth, gopherheight, "Text Document", resizable=1, pumpcall=newgop.pumpcall1, xpos=20))



#gopher menu class. also used for text documents
class gopherpane:
	def __init__(self, host='about:splash', port=70, selector="", prefix="menu: gopher://", preload=None, forceimage=0, linkdisable=0, gtype="1", shortprefix="menu: ", loading=1):
		self.host=host
		self.port=port
		self.selector=selector
		self.yoff=25
		self.yjump=int(libzox.cnfdict["menutextjump"])
		self.menu=[]
		self.images=[]
		self.data=None
		self.prefix=prefix
		self.preload=preload
		self.forceimage=forceimage
		self.linkdisable=linkdisable
		self.renderdict={}
		self.gtype=gtype
		self.shortprefix=shortprefix
		self.bookbtn=bookbtn.convert()
		self.menucorner=menucorner.convert()
		self.menucorner_wait=menucorner_wait.convert()
		self.rootbtn=rootbtn.convert()
		self.rootbtn_inact=rootbtn_inact.convert()
		self.loadbtn=loadbtn.convert()
		self.loadbtn_inact=loadbtn_inact.convert()
		self.histlist=[]
		self.histpoint=-1
		self.scrollup=scrollup.convert()
		self.scrolldn=scrolldn.convert()
		self.scrollup_no=scrollup_no.convert()
		self.scrolldn_no=scrolldn_no.convert()
		self.backbtn=backbtn.convert()
		self.backbtn_inact=backbtn_inact.convert()
		self.nextbtn=nextbtn.convert()
		self.nextbtn_inact=nextbtn_inact.convert()
		self.upbtn=upbtn.convert()
		self.upbtn_inact=upbtn_inact.convert()
		self.loading=loading
	#menu get routine
	def menuget(self):
		
		
		self.data=pathfigure(self.host, self.port, self.selector, self.gtype)
		self.menu=libgop.menudecode(self.data)
		for item in self.renderdict:
			del item
		del self.renderdict
		#print("newhist")
		self.renderdict={}
		self.histlist=self.histlist[:self.histpoint+1]
		self.histlist.extend([libzox.histitem(self.host, self.port, self.selector, self.gtype, self.data, self.menu)])
		self.histpoint+=1
		if len(self.histlist)==histsize+1:
			#print("histpop")
			self.histlist.pop(0)
			self.histpoint-=1
	def menuget_nohist(self):
		
		
		self.data=pathfigure(self.host, self.port, self.selector, self.gtype)
		self.menu=libgop.menudecode(self.data)
		for item in self.renderdict:
			del item
		del self.renderdict
		self.renderdict={}
	def newhist(self):
		#print("newhist")
		self.histlist=self.histlist[:self.histpoint+1]
		self.histlist.extend([libzox.histitem(self.host, self.port, self.selector, self.gtype, self.data, self.menu)])
		self.histpoint+=1
		if len(self.histlist)==histsize+1:
			#print("histpop")
			self.histlist.pop(0)
			self.histpoint-=1
	#render routine
			
	def menudraw(self, frameobj):
		imageset=[]
		imagecount=0
		self.ypos=self.yoff
		frameobj.surface.fill((255, 255, 255))
		self.siderect=pygame.Rect(0, 0, 25, frameobj.surface.get_height())
		#pygame.draw.rect(frameobj.surface, (185, 195, 255), self.siderect)
		pygame.draw.rect(frameobj.surface, (223, 223, 223), self.siderect)
		pygame.draw.line(frameobj.surface, (0, 0, 0), (25, 0), (25, frameobj.surface.get_height()), 1)
		for item in self.menu:
			if item.gtype=="3":
				rects, self.ypos, self.renderdict = textitem(item.name, simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.ypos, self.renderdict, gterror)
			elif item.gtype=="i" or item.gtype==None:
				rects, self.ypos, self.renderdict = textitem(item.name, simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.ypos, self.renderdict)
			elif item.gtype=="1" and item.hostname.startswith("about:"):
				rect, self.ypos, self.renderdict = textitem(item.name, linkfont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtmenuint, 1)
				item.rect=rect
			elif item.gtype=="1" and item.hostname!=self.host:
				rect, self.ypos, self.renderdict = textitem(item.name, linkfont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtmenuremote, 1)
				item.rect=rect
			elif item.gtype=="1" and (item.selector=="/" or item.selector==""):
				rect, self.ypos, self.renderdict = textitem(item.name, linkfont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtmenuroot, 1)
				item.rect=rect
			elif item.gtype=="1":
				rect, self.ypos, self.renderdict = textitem(item.name, linkfont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtmenu, 1)
				item.rect=rect
			elif item.gtype=="7":
				rect, self.ypos, self.renderdict = textitem(item.name, linkfont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtquery, 1)
				item.rect=rect
			elif item.gtype=="0":
				rect, self.ypos, self.renderdict = textitem(item.name, linkfont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gttext, 1)
				item.rect=rect
			#image preview routine
			
			elif item.gtype=="g" or item.gtype=="p" or item.gtype=="I":
				imagecount+=1
				try:
					if item.image!=None:
						
						rectia, self.ypos, self.renderdict = textitem(item.name, simplefont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtimage, 1)
						rectib=frameobj.surface.blit(item.image, (26, self.ypos))
						item.rect=rectia.unionall([rectib])
						#pygame.draw.rect(frameobj.surface, (60, 60, 255), item.rect, 1)
						self.ypos+=item.image.get_height()
					if item.image==None:
						item.rect, self.ypos, self.renderdict = textitem(item.name, simplefont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtimage, 1)
					#pygame.draw.rect(frameobj.surface, (255, 255, 0), item.rect, 1)
				except AttributeError as err:
					#print(err)
					item.image=None
					if imagecount<maximages or (imagecount<2 and self.forceimage) or self.host.startswith("about:"):
						imageset.extend([item])
					item.rect, self.ypos, self.renderdict = textitem(item.name, simplefont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtimage, 1)
			elif item.gtype=="s":
				item.rect, self.ypos, self.renderdict = textitem(item.name, linkfont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtsound, 1)
			
			
			
			elif item.gtype=="9":
				rect, self.ypos, self.renderdict = textitem("[NS]"+item.name, linkfont, self.yjump, (30, 0, 0), frameobj.surface, self.ypos, self.renderdict, gtbin, 1)
			
			elif item.gtype=="h":
				item.rect, self.ypos, self.renderdict = textitem(item.name, linkfont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtweb, 1)

			else:
				rects, self.ypos, self.renderdict = textitem("[NS:" + item.gtype + "]" + item.name, simplefont, 15, (0, 0, 0), frameobj.surface, self.ypos, self.renderdict)
				#print(item.gtype)
			if libzox.itemdebug:
				try:
					pygame.draw.rect(frameobj.surface, (255, 0, 0), item.rect, 1)
				except AttributeError:
					pass
		#launch image loader thread if needed
		if imageset!=[]:
			self.images=imageset
			self.loading=1
			sideproc=Thread(target = imgget, args = [imageset, self.menudraw, frameobj, self])
			sideproc.daemon=True
			sideproc.start()
		self.hudrect=pygame.Rect(0, 0, frameobj.surface.get_width(), 22)
		pygame.draw.rect(frameobj.surface, (60, 60, 120), self.hudrect)
		#self.hudcorner=pygame.Rect(0, 0, 25, 22)
		#pygame.draw.rect(frameobj.surface, (255, 255, 255), self.hudcorner)
		if self.loading:
			frameobj.surface.blit(self.menucorner_wait, (0, 0))
		else:
			frameobj.surface.blit(self.menucorner, (0, 0))
		xpos=27
		if self.histpoint>0 and self.loading==0:
			self.backrect=frameobj.surface.blit(self.backbtn, (xpos, 1))
		else:
			self.backrect=frameobj.surface.blit(self.backbtn_inact, (xpos, 1))
		xpos+=60
		if self.histpoint<len(self.histlist)-1 and self.loading==0:
			self.nextrect=frameobj.surface.blit(self.nextbtn, (xpos, 1))
		else:
			self.nextrect=frameobj.surface.blit(self.nextbtn_inact, (xpos, 1))
		xpos+=60
		if "/" in self.selector and self.selector!="/":
			self.uprect=frameobj.surface.blit(self.upbtn, (xpos, 1))
		else:
			self.uprect=frameobj.surface.blit(self.upbtn_inact, (xpos, 1))
		xpos+=60
		if self.selector!="/" and self.selector!="":
			self.rootrect=frameobj.surface.blit(self.rootbtn, (xpos, 1))
		else:
			self.rootrect=frameobj.surface.blit(self.rootbtn_inact, (xpos, 1))
		xpos+=62
		pygame.draw.line(frameobj.surface, (255, 255, 255), (xpos, 0), (xpos, 25), 2)
		xpos+=8
		self.bookrect=frameobj.surface.blit(self.bookbtn, (xpos, 1))
		xpos+=60
		if self.loading:
			self.loadrect=frameobj.surface.blit(self.loadbtn_inact, (xpos, 1))
		else:
			self.loadrect=frameobj.surface.blit(self.loadbtn, (xpos, 1))
		
		
		if self.yoff<25:
			self.scuprect=frameobj.surface.blit(self.scrollup, (frameobj.surface.get_width()-44, 0))
		else:
			self.scuprect=frameobj.surface.blit(self.scrollup_no, (frameobj.surface.get_width()-44, 0))
		if self.ypos>frameobj.sizey:
			self.scdnrect=frameobj.surface.blit(self.scrolldn, (frameobj.surface.get_width()-88, 0))
		else:
			self.scdnrect=frameobj.surface.blit(self.scrolldn_no, (frameobj.surface.get_width()-88, 0))
		
	#menu change loader
	def menuchange(self, item, frameobj):
		self.host=item.hostname
		self.port=item.port
		self.selector=item.selector
		if self.host.startswith("about:help"):
			frameobj.name=("help: "+str(self.host))
		elif item.hostname.startswith("about:"):
			frameobj.name=(self.shortprefix+str(item.hostname))
		else:
			frameobj.name=(self.prefix+str(item.hostname) + "/" + self.gtype + str(item.selector))
		self.menuget()
		self.yoff=25
		self.loading=0
		self.menudraw(frameobj)
		return
	def menurefresh(self, frameobj):
		#self.histpoint-=1
		self.menuget_nohist()
		#refresh history entry of the current page.
		histref=self.histlist[self.histpoint]
		histref.menu=self.menu
		histref.data=self.data
		self.yoff=25
		self.loading=0
		self.menudraw(frameobj)
	def menuroot(self, frameobj):
		self.selector="/"
		self.gtype="1"
		#reset prefixes in case of text document being the current.
		self.prefix="menu: gopher://"
		self.shortprefix="menu: "
		if self.host.startswith("about:"):
			frameobj.name=(self.shortprefix+str(self.host))
		else:
			frameobj.name=(self.prefix+str(self.host) + "/" + self.gtype + str(self.selector))
		self.menuget()
		self.yoff=25
		self.loading=0
		self.menudraw(frameobj)
	def menuup(self, frameobj):
		if self.selector.count("/")>1 and not self.selector.endswith("/"):
			self.selector=self.selector.rsplit("/", 1)[0]
		elif self.selector.count("/")>2 and self.selector.endswith("/"):
			self.selector=self.selector.rsplit("/", 2)[0]
		else:
			self.selector="/"
		self.gtype="1"
		#reset prefixes in case of text document being the current.
		self.prefix="menu: gopher://"
		self.shortprefix="menu: "
		if self.host.startswith("about:"):
			frameobj.name=(self.shortprefix+str(self.host))
		else:
			frameobj.name=(self.prefix+str(self.host) + "/" + self.gtype + str(self.selector))
		self.menuget()
		self.yoff=25
		self.loading=0
		self.menudraw(frameobj)
	#menu initalization loader
	def menuinital(self, frameobj):
		if self.host.startswith("about:help"):
			frameobj.name=("help: "+str(self.host))
		elif self.host.startswith("about:"):
			frameobj.name=(self.shortprefix+str(self.host))
		else:
			frameobj.name=(self.prefix+str(self.host) + "/" + self.gtype + str(self.selector))
		self.menuget()
		self.yoff=25
		self.loading=0
		self.menudraw(frameobj)
	def histchange(self, histitem, frameobj):
		self.data=histitem.data
		self.menu=histitem.menu
		self.host=histitem.host
		self.port=histitem.port
		self.selector=histitem.selector
		self.gtype=histitem.gtype
		if histitem.gtype=="0":
			self.prefix="text: gopher://"
		else:
			self.prefix="menu: gopher://"
		self.shortprefix="menu: "
		if self.host.startswith("about:help"):
			frameobj.name=("help: "+str(self.host))
		elif self.host.startswith("about:"):
			frameobj.name=(self.shortprefix+str(self.host))
		else:
			frameobj.name=(self.prefix+str(self.host) + "/" + self.gtype + str(self.selector))
		self.renderdict={}
		self.yoff=25
		self.menudraw(frameobj)
		
	def pumpcall1(self, frameobj, data=None):
		
		#link destination preview routine. 
		if frameobj.statflg==0 and frameobj.wo==0 and frameobj.shade==0:
			mpos=stz.mousehelper(pygame.mouse.get_pos(), frameobj)
			if self.loadrect.collidepoint(mpos):
				deskt.hovertext="Reload this menu. (CTRL+r)"
			elif self.rootrect.collidepoint(mpos):
				deskt.hovertext="Goto server root. (ALT+down)"
			elif self.bookrect.collidepoint(mpos):
				deskt.hovertext="Bookmark this menu. (m)"
			elif self.backrect.collidepoint(mpos):
				deskt.hovertext="Previous menu in history. (ALT+left)"
			elif self.nextrect.collidepoint(mpos):
				deskt.hovertext="Next menu in history. (ALT+right)"
			elif self.uprect.collidepoint(mpos):
				deskt.hovertext="Go up a level. (ALT+up)"
			elif self.scuprect.collidepoint(mpos):
				deskt.hovertext="If not greyed out, you may scroll up."
			elif self.scdnrect.collidepoint(mpos):
				deskt.hovertext="If not greyed out, you may scroll down."
			elif not self.hudrect.collidepoint(mpos):
				for item in self.menu:
					if item.gtype!=None:
						if item.gtype in "01pgI7s":
							try:
								if item.rect.collidepoint(mpos):
									if item.hostname.startswith("about:"):
										deskt.hovertext=(item.hostname)
									else:
										deskt.hovertext=("gopher://" + item.hostname + "/" + item.gtype + item.selector)
									break
							except AttributeError:
								continue
						if item.gtype=="h":
							try:
								if item.rect.collidepoint(mpos):
									deskt.hovertext=item.selector
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
			self.menudraw(frameobj)
			if self.preload==None:
				sideproc=Thread(target = self.menuinital, args = [frameobj])
				sideproc.daemon=True
				sideproc.start()
			else:
				self.menu=self.preload
				self.menudraw(frameobj)
				if self.host.startswith("about:help"):
					frameobj.name=("help: "+str(self.host))
				elif self.host.startswith("about:"):
					frameobj.name=(self.shortprefix+str(self.host))
				else:
					frameobj.name=(self.prefix+str(self.host) + "/" + self.gtype + str(self.selector))
				self.newhist()
		#resize
		if frameobj.statflg==2:
			self.yoff=25
			for item in self.renderdict:
				del item
			del self.renderdict
			self.renderdict={}
			libzox.reshrinkimages(self.images, frameobj)
			self.menudraw(frameobj)
		
		if frameobj.statflg==6:
			if data.key==pygame.K_UP:
				self.yoff+=self.yjump*2
				if self.yoff>25:
					self.yoff=25
				self.menudraw(frameobj)
			if data.key==pygame.K_DOWN and self.ypos>frameobj.sizey:
				self.yoff-=self.yjump*2
				self.menudraw(frameobj)
			if data.key==pygame.K_m:
				newgop=bookmadded(url=libzox.gurlencode(self.host, self.selector, self.gtype, self.port))
				framesc.add_frame(stz.framex(500, 100, "New Bookmark", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50))
			mods=pygame.key.get_mods()
			if mods & pygame.KMOD_CTRL:
				if data.key==pygame.K_r:
					if not self.loading:
						self.loading=1
						self.menudraw(frameobj)
						sideproc=Thread(target = self.menurefresh, args = [frameobj])
						sideproc.daemon=True
						sideproc.start()
			if mods & pygame.KMOD_ALT:
				if data.key==pygame.K_LEFT:
					if self.histpoint>0:
						self.histpoint-=1
						self.histchange(self.histlist[self.histpoint], frameobj)
				elif data.key==pygame.K_RIGHT:
					if self.histpoint<len(self.histlist)-1:
						self.histpoint+=1
						self.histchange(self.histlist[self.histpoint], frameobj)
				elif data.key==pygame.K_UP:
					if "/" in self.selector and self.selector!="/":
						self.loading=1
						self.menudraw(frameobj)
						sideproc=Thread(target = self.menuup, args = [frameobj])
						sideproc.daemon=True
						sideproc.start()
				elif data.key==pygame.K_DOWN:
					if self.selector!="/" and self.selector!="":
						self.loading=1
						self.menudraw(frameobj)
						sideproc=Thread(target = self.menuroot, args = [frameobj])
						sideproc.daemon=True
						sideproc.start()
		#mouse button down
		if frameobj.statflg==4:
			if self.hudrect.collidepoint(stz.mousehelper(data.pos, frameobj)):
				#print("Blocked")
				if data.button==3:
					if self.rootrect.collidepoint(stz.mousehelper(data.pos, frameobj)):
						if self.selector!="/" and self.selector!="":
							self.loading=1
							self.menudraw(frameobj)
							newgop=gopherpane(host=self.host, port=self.port, selector="/")
							framesc.add_frame(stz.framex(gopherwidth, gopherheight, "Gopher Menu", resizable=1, pumpcall=newgop.pumpcall1))
				if data.button==1:
					if self.loadrect.collidepoint(stz.mousehelper(data.pos, frameobj)):
						if not self.loading:
							self.loading=1
							self.menudraw(frameobj)
							sideproc=Thread(target = self.menurefresh, args = [frameobj])
							sideproc.daemon=True
							sideproc.start()
					if self.rootrect.collidepoint(stz.mousehelper(data.pos, frameobj)):
						if self.selector!="/" and self.selector!="":
							self.loading=1
							self.menudraw(frameobj)
							sideproc=Thread(target = self.menuroot, args = [frameobj])
							sideproc.daemon=True
							sideproc.start()
					if self.bookrect.collidepoint(stz.mousehelper(data.pos, frameobj)):
						newgop=bookmadded(url=libzox.gurlencode(self.host, self.selector, self.gtype, self.port))
						framesc.add_frame(stz.framex(500, 100, "New Bookmark", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50))
					if self.backrect.collidepoint(stz.mousehelper(data.pos, frameobj)):
						if self.histpoint>0 and self.loading==0:
							self.histpoint-=1
							self.histchange(self.histlist[self.histpoint], frameobj)
					if self.nextrect.collidepoint(stz.mousehelper(data.pos, frameobj)):
						if self.histpoint<len(self.histlist)-1 and self.loading==0:
							self.histpoint+=1
							self.histchange(self.histlist[self.histpoint], frameobj)
					if self.uprect.collidepoint(stz.mousehelper(data.pos, frameobj)):
						if "/" in self.selector and self.selector!="/":
							self.loading=1
							self.menudraw(frameobj)
							sideproc=Thread(target = self.menuup, args = [frameobj])
							sideproc.daemon=True
							sideproc.start()
							
						
			elif data.button==1 and not self.linkdisable:
				for item in self.menu:
					mods=pygame.key.get_mods()
					
					if mods & pygame.KMOD_SHIFT:
						if item.gtype!=None:
							if item.gtype in "10gpI7s":
								if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
									newgop=bookmadded(url=libzox.gurlencode(item.hostname, item.selector, item.gtype, item.port), name=item.name)
									framesc.add_frame(stz.framex(500, 100, "New Bookmark", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50))

					else:
						
						if item.gtype=="1":
							if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
								self.menu=[]
								self.loading=1
								self.menudraw(frameobj)
								sideproc=Thread(target = self.menuchange, args = [item, frameobj])
								sideproc.daemon=True
								sideproc.start()
								break
						if item.gtype=="0":
							if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
								#sideproc=Thread(target = textshow, args = [item.hostname, item.port, item.selector])
								#sideproc.daemon=True
								#sideproc.start()
								#break
								self.menu=[]
								self.loading=1
								self.gtype="0"
								self.prefix="text: gopher://"
								self.menudraw(frameobj)
								sideproc=Thread(target = self.menuchange, args = [item, frameobj])
								sideproc.daemon=True
								sideproc.start()
								break
						if item.gtype=="g" or item.gtype=="p" or item.gtype=="I":
							if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
								#itemcopy=copy.deepcopy(item)
								#del itemcopy.image
								#newgop=gopherpane(host=itemcopy.hostname, port=itemcopy.port, selector=itemcopy.selector, prefix="image: gopher://", preload=[itemcopy], forceimage=1, linkdisable=1, gtype=item.gtype, shortprefix="image: ")
								newgop=imgview(host=item.hostname, port=item.port, selector=item.selector, gtype=item.gtype, imagesurf=item.fullimage)
								framesc.add_frame(stz.framex(500, 400, "Image", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50))
						if item.gtype=="7":
							if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
								newgop=querypane(host=item.hostname, port=item.port, selector=item.selector)
								framesc.add_frame(stz.framex(500, 100, "Gopher Query", resizable=1, pumpcall=newgop.pumpcall1))
						if item.gtype=="s":
							if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
								newgop=sndplay(item.hostname, item.port, item.selector)
								framesc.add_frame(stz.framex(500, 100, "Sound", resizable=1, pumpcall=newgop.pumpcall1))
						if item.gtype=="h":
							if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
								print(item.selector)
								browscmd=libzox.cnfdict["browser"]
								if browscmd not in ["", "none"]:
									try:
										Popen([browscmd, item.selector.replace("URL:", "")])
									except OSError:
										print("Can't open web browser!")
								else:
									print("Web browser not configured!")

			elif data.button==3 and not self.linkdisable:
				for item in self.menu:
					if item.gtype=="1":
						if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
							newgop=gopherpane(host=item.hostname, port=item.port, selector=item.selector)
							framesc.add_frame(stz.framex(gopherwidth, gopherheight, "Gopher Menu", resizable=1, pumpcall=newgop.pumpcall1))
					if item.gtype=="0":
						if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
							newgop=gopherpane(host=item.hostname, port=item.port, selector=item.selector, gtype="0", prefix="text: gopher://")
							framesc.add_frame(stz.framex(gopherwidth, gopherheight, "Gopher Menu", resizable=1, pumpcall=newgop.pumpcall1))
			elif data.button==4:
				self.yoff+=self.yjump*2
				if self.yoff>25:
					self.yoff=25
				self.menudraw(frameobj)
			elif data.button==5 and self.ypos>frameobj.sizey:
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
		self.yjump=int(libzox.cnfdict["menutextjump"])
		self.stringblob=""
		if self.host=="QUERYTEST":
			self.debug=1
		else:
			self.debug=0
		self.validchars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890"
	def renderdisp(self, frameobj):
		str1=self.host+"/7"+self.selector
		frameobj.surface.fill((255, 255, 255))
		textitem(str1, simplefont, self.yjump, (0, 0, 0), frameobj.surface, 0, {}, xoff=0)
		textitem("Please Type Query", simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.yjump*2, {}, xoff=0)
		textitem(">"+self.stringblob+"|", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*4, {}, xoff=0)
	def loader(self, frameobj):
		frameobj.name="Loading..."
		try:
			data=libgop.gopherget(self.host, self.port, self.selector, query=self.stringblob)
		except Exception as err:
			print(err)
			data=open(os.path.join("vgop", "gaierror"))
		menu=libgop.menudecode(data)
		newgop=gopherpane(host=self.host, port=self.port, selector=self.selector, preload=menu, loading=0)
		framesc.add_frame(stz.framex(gopherwidth, gopherheight, "Gopher Menu", resizable=1, pumpcall=newgop.pumpcall1))
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
		self.yjump=int(libzox.cnfdict["menutextjump"])
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
		self.scrollup=scrollup.convert()
		self.scrolldn=scrolldn.convert()
		self.scrollup_no=scrollup_no.convert()
		self.scrolldn_no=scrolldn_no.convert()
		if self.bookm!=None:
			self.urlblob=self.bookm.url
			self.nameblob=self.bookm.name
		self.del0=bookm_del0.convert()
		self.del1=bookm_del1.convert()
		self.go0=bookm_go0.convert()
		self.go1=bookm_go1.convert()
		self.edit0=bookm_edit0.convert()
		self.edit1=bookm_edit1.convert()
		self.newbm=bookm_newbm.convert()
		self.menucorner_book=menucorner_book.convert()
		self.funct=0
		self.bmprev=None
		self.offset=0
	def loaderg1(self, frameobj):
		newgop=gopherpane(host=self.host, port=self.port, selector=self.selector)
		framesc.add_frame(stz.framex(gopherwidth, gopherheight, "Gopher Menu", resizable=1, pumpcall=newgop.pumpcall1))
		#close self
		self.offset=0
	def loaderg0(self, frameobj):
		newgop=gopherpane(host=self.host, port=self.port, selector=self.selector, gtype="0", prefix="text: gopher://")
		framesc.add_frame(stz.framex(gopherwidth, gopherheight, "Gopher Menu", resizable=1, pumpcall=newgop.pumpcall1))
	def renderdisp(self, frameobj):
		
		if self.offset>0:
			xlist=bmlist[self.offset:]
		else:
			xlist=bmlist
		frameobj.surface.fill((255, 255, 255))
		self.siderect=pygame.Rect(0, 0, 25, frameobj.surface.get_height())
		#pygame.draw.rect(frameobj.surface, (185, 195, 255), self.siderect)
		pygame.draw.rect(frameobj.surface, (223, 223, 223), self.siderect)
		pygame.draw.line(frameobj.surface, (0, 0, 0), (25, 0), (25, frameobj.surface.get_height()), 1)
		pygame.draw.rect(frameobj.surface, (60, 60, 120), pygame.Rect(0, 0, frameobj.surface.get_width(), 22))
		frameobj.surface.blit(self.menucorner_book, (0, 0))
		self.newrect=frameobj.surface.blit(self.newbm, (176, 1))
		if self.funct==0:
			self.gorect=frameobj.surface.blit(self.go1, (26, 1))
			self.delrect=frameobj.surface.blit(self.del0, (76, 1))
			self.editrect=frameobj.surface.blit(self.edit0, (126, 1))
		elif self.funct==1:
			self.gorect=frameobj.surface.blit(self.go0, (26, 1))
			self.delrect=frameobj.surface.blit(self.del1, (76, 1))
			self.editrect=frameobj.surface.blit(self.edit0, (126, 1))
		else:
			self.gorect=frameobj.surface.blit(self.go0, (26, 1))
			self.delrect=frameobj.surface.blit(self.del0, (76, 1))
			self.editrect=frameobj.surface.blit(self.edit1, (126, 1))
		self.ypos=25
		for item in xlist:
			item.rect, self.ypos, self.renderdict = textitem(item.name, linkfont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, itemicn=self.getitemtypeicn(item.url), link=1)
			if libzox.itemdebug:
				try:
					pygame.draw.rect(frameobj.surface, (255, 0, 0), item.rect, 1)
				except AttributeError:
					pass
		if self.offset>0:
			self.scuprect=frameobj.surface.blit(self.scrollup, (frameobj.surface.get_width()-44, 0))
		else:
			self.scuprect=frameobj.surface.blit(self.scrollup_no, (frameobj.surface.get_width()-44, 0))
		if self.ypos>frameobj.sizey:
			self.scdnrect=frameobj.surface.blit(self.scrolldn, (frameobj.surface.get_width()-88, 0))
		else:
			self.scdnrect=frameobj.surface.blit(self.scrolldn_no, (frameobj.surface.get_width()-88, 0))
	def getitemtypeicn(self, url):
		gtype=libzox.gurldecode(url)[3]
		selector=libzox.gurldecode(url)[2]
		if gtype=="1":
			if selector=="" or selector=="/":
				return gtmenuroot
			else:
				return gtmenu
		if gtype=="0":
			return gttext
		if gtype=="7":
			return gtquery
		if gtype=="s":
			return gtsound
		if gtype=="g" or gtype=="p" or gtype=="I":
			return gtimage
		return None
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
			framesc.add_frame(stz.framex(500, 100, "Gopher Query", resizable=1, pumpcall=newgop.pumpcall1))
		elif self.gtype=="g" or self.gtype=="p" or self.gtype=="I":
			newgop=imgview(host=self.host, port=self.port, selector=self.selector, gtype=self.gtype)
			framesc.add_frame(stz.framex(500, 400, "Image", resizable=1, pumpcall=newgop.pumpcall1))
		elif self.gtype=="s":
			newgop=sndplay(self.host, self.port, self.selector)
			framesc.add_frame(stz.framex(500, 100, "Sound", resizable=1, pumpcall=newgop.pumpcall1))
	def deldiagret(self, flag, carrydata):
		if flag:
			if carrydata in bmlist:
				bmlist.remove(carrydata)
				libzox.bmsave(bmlist)
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==2:
			self.offset=0
			self.renderdisp(frameobj)
		if frameobj.statflg==0 and self.bmprev!=bmlist:
			self.bmprev=list(bmlist)
			self.offset=0
			self.renderdisp(frameobj)
		if frameobj.statflg==0 and frameobj.wo==0 and frameobj.shade==0:
			mpos=pygame.mouse.get_pos()
			for item in bmlist:
				if item.rect.collidepoint(stz.mousehelper(mpos, frameobj)):
					if item.url.startswith("about:"):
						deskt.hovertext=item.url
					else:
						deskt.hovertext="gopher://" + item.url
			if self.newrect.collidepoint(stz.mousehelper(mpos, frameobj)):
				deskt.hovertext="Create a new bookmark."
			if self.editrect.collidepoint(stz.mousehelper(mpos, frameobj)):
				deskt.hovertext="Edit a bookmark."
			if self.delrect.collidepoint(stz.mousehelper(mpos, frameobj)):
				deskt.hovertext="Delete a bookmark."
			if self.gorect.collidepoint(stz.mousehelper(mpos, frameobj)):
				deskt.hovertext="Open a bookmark in a new window."
			elif self.scuprect.collidepoint(stz.mousehelper(mpos, frameobj)):
				deskt.hovertext="If not greyed out, you may scroll up."
			elif self.scdnrect.collidepoint(stz.mousehelper(mpos, frameobj)):
				deskt.hovertext="If not greyed out, you may scroll down."
		if frameobj.statflg==1:
			frameobj.name="Bookmarks"
			self.renderdisp(frameobj)
		if frameobj.statflg==4:
			if data.button==4:
				self.offset-=1
				if self.offset<0:
					self.offset=0
				self.renderdisp(frameobj)
			if data.button==5:
				if self.ypos>frameobj.sizey:
					self.offset+=1
					if self.offset>len(bmlist)-1 and len(bmlist)>0:
						self.offset=len(bmlist)-1
					self.renderdisp(frameobj)
			if data.button==1:
				if self.newrect.collidepoint(stz.mousehelper(data.pos, frameobj)):
					newgop=bookmadded()
					framesc.add_frame(stz.framex(500, 100, "New Bookmark", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50))
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
							libzoxui.do_yndialog("Delete Bookmark? (" + item.name + ")", "name: " + item.name + "\ngopher://" + item.url, self.deldiagret, canclose=1, carrydata=item)
						if self.funct==2:
							newgop=bookmadded(bookm=item)
							framesc.add_frame(stz.framex(500, 100, "Edit Bookmark", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50))
		



#bookmark creator/editor dialog.
class bookmadded:
	def __init__(self, url="", bookm=None, name=""):
		self.yoff=0
		self.yjump=int(libzox.cnfdict["menutextjump"])
		self.stringblob=""
		#self.hovmsg="Enter a gopher URL to load."
		self.validchars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890:/.-_ "
		#self.url=url
		self.bookm=bookm
		self.url=url
		#self.mode=mode
		self.urlblob=url
		self.nameblob=name
		if self.bookm!=None:
			self.urlblob=self.bookm.url
			self.nameblob=self.bookm.name
		self.line=1
	def renderdisp(self, frameobj):
		frameobj.surface.fill((255, 255, 255))
		textitem("tab=switch entries, enter=accept", simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.yjump*1, {}, xoff=0)
		if self.line:
			textitem("gopher://"+self.urlblob+"", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*3, {}, xoff=0)
			textitem("name:"+self.nameblob+"|", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*5, {}, xoff=0)
		else:
			textitem("gopher://"+self.urlblob+"|", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*3, {}, xoff=0)
			textitem("name:"+self.nameblob+"", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*5, {}, xoff=0)
	
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




#url entry dialog box.
class urlgo:
	def __init__(self):
		self.yoff=0
		self.yjump=int(libzox.cnfdict["menutextjump"])
		self.stringblob=""
		#self.hovmsg="Enter a gopher URL to load."
		self.validchars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890:/.-_"
	def renderdisp(self, frameobj):
		frameobj.surface.fill((255, 255, 255))
		textitem("Please Type URL", simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.yjump*2, {}, xoff=0)
		textitem("gopher://"+self.stringblob+"|", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*4, {}, xoff=0)
	def loaderg1(self, frameobj):
		newgop=gopherpane(host=self.host, port=self.port, selector=self.selector)
		framesc.add_frame(stz.framex(gopherwidth, gopherheight, "Gopher Menu", resizable=1, pumpcall=newgop.pumpcall1))
		#close self
		self.offset=0
	def loaderg0(self, frameobj):
		newgop=gopherpane(host=self.host, port=self.port, selector=self.selector, gtype="0", prefix="text: gopher://")
		framesc.add_frame(stz.framex(gopherwidth, gopherheight, "Gopher Menu", resizable=1, pumpcall=newgop.pumpcall1))
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
						framesc.add_frame(stz.framex(350, 100, "Gopher Query", resizable=1, pumpcall=newgop.pumpcall1))
						framesc.close_pid(frameobj.pid)
					elif self.gtype=="s":
						newgop=sndplay(self.host, self.port, self.selector)
						framesc.add_frame(stz.framex(500, 100, "Sound", resizable=1, pumpcall=newgop.pumpcall1))
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
		self.maxsize=int(libzox.cnfdict["viewzoom"])
		self.dummysurf=pygame.image.load(os.path.join("vgop", "loadingimage.png"))
		if self.imagesurf==None:
			self.surf=self.dummysurf
			sideproc=Thread(target = self.imageload)
			sideproc.daemon=True
			sideproc.start()
		else:
			self.surf=libzox.imagelimit(self.imagesurf, self.maxsize)
	
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
			self.surf=libzox.imagelimit(self.surf, self.maxsize)
		except pygame.error:
			self.surf=pygame.image.load(os.path.join("vgop", "giaerror.png"))
			print("imgview: Failed to load.")
			
		self.loaderupt=1
		
	def updatedisp(self, frameobj):
		if self.pscf!=self.scf:
			self.surftran=pygame.transform.scale(self.surf, ((int(self.imgx * self.scf)), (int(self.imgy * self.scf))))
			self.surftran.convert_alpha()
			self.pscf=self.scf
		self.imgbox = self.surftran.get_rect()
		self.imgbox.centerx = int(self.xoff)
		self.imgbox.centery = int(self.yoff)
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
			self.xoff=self.surfx/2.0
			self.yoff=self.surfy/2.0
			if scfx>scfy:
				scf=scfy
			else:
				scf=scfx
			#limit default zoom to maxsize
			while scf*self.imgx>self.maxsize or scf*self.imgx>self.maxsize:
				scf/=1.1
			self.scfdef=scf
			self.scf=scf
			self.updatedisp(frameobj)
		if frameobj.statflg==4:
			
			if data.button==5:
				self.scf/=1.1
				if self.scf<0.1:
					self.scf=0.1
				else:
					gpos=stz.mousehelper(data.pos, frameobj)
					self.yoff=((self.yoff-gpos[1])/1.1)+gpos[1]
					self.xoff=((self.xoff-gpos[0])/1.1)+gpos[0]
				
			if data.button==4:
				#ensure new zoom level doesn't exceed maxsize setting.
				if not (self.scf*1.1*self.imgx>self.maxsize or self.scf*1.1*self.imgx>self.maxsize):
					self.scf*=1.1
					if self.scf>20.0:
						self.scf=20.0
					
					else:
						gpos=stz.mousehelper(data.pos, frameobj)
						self.yoff=((self.yoff-gpos[1])*1.1)+gpos[1]
						self.xoff=((self.xoff-gpos[0])*1.1)+gpos[0]
				
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

#basic routine for quitting.
class quitx:
	def __init__(self):
		return
	def pumpcall1(self, frameobj, data=None):
		pygame.event.clear()
		pygame.event.post(pygame.event.Event(pygame.QUIT))
		framesc.close_frame(frameobj)


class sndplay:
	def __init__(self, host, port, selector):
		self.yoff=0
		self.yjump=int(libzox.cnfdict["menutextjump"])
		self.host=host
		self.port=port
		self.selector=selector
		self.gtype='s'
		self.data=0
	def renderdisp(self, frameobj):
		frameobj.surface.fill((255, 255, 255))
		textitem("[p] play/restart, [s] stop", simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.yjump*2, {}, xoff=0)
		textitem("sound: gopher://"+libzox.gurlencode(self.host, self.selector, self.gtype, self.port), simplefont, self.yjump, (0, 0, 0), frameobj.surface, 0, {}, xoff=0)
	def loader(self, frameobj):
		try:
			data=pathfigure(self.host, self.port, self.selector, gtype='s')
			if data!=None and data!=0:
				pygame.mixer.music.load(data)
				pygame.mixer.music.play(-1)
				frameobj.name="sound: playing"
				self.data=data
			if data==None:
				frameobj.name="sound: ZERROR: aud1"
		except pygame.error:
			frameobj.name="sound: ZERROR: aud0"
			return
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==2:
			self.renderdisp(frameobj)
		if frameobj.statflg==1:
			frameobj.name="sound: loading... Please wait."
			self.renderdisp(frameobj)
			sideproc=Thread(target = self.loader, args = [frameobj])
			sideproc.daemon=True
			sideproc.start()
		if frameobj.statflg==3:
			try:
				pygame.mixer.music.stop()
			except pygame.error:
				return
		if frameobj.statflg==6:
			if data.key==pygame.K_p:
				try:
					self.data.seek(0)
					
					pygame.mixer.music.load(self.data)
					pygame.mixer.music.play(-1)
					frameobj.name="sound: playing"
				except pygame.error:
					return
			if data.key==pygame.K_s:
				try:
					frameobj.name="sound: stopped"
					pygame.mixer.music.stop()
					
				except pygame.error:
					return
				
				

