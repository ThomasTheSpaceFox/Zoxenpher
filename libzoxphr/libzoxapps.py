#!/usr/bin/env python
#import time
import os
import sys
from . import libgop
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
import time

simplefont = pygame.font.SysFont(libzox.cnfdict["menufont"], int(libzox.cnfdict["menufontsize"]))
linkfont = pygame.font.SysFont(libzox.cnfdict["menufont"], int(libzox.cnfdict["menufontsize"]))
morefonthead = pygame.font.SysFont(None, 22)
morefontcomment = pygame.font.SysFont(None, 19)
linkfont.set_underline(1)
tilestr=libzox.cnfdict["bgtile"]
if tilestr=="none":
	tiledraw=None
else:
	try:
		tiledraw=pygame.image.load(os.path.join(libzox.gfxpath, tilestr))
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
bookbtn=pygame.image.load(os.path.join(libzox.gfxpath, "bookbtn.png"))
menucorner=pygame.image.load(os.path.join(libzox.gfxpath, "menucorner.png"))
menucorner_wait=pygame.image.load(os.path.join(libzox.gfxpath, "menucorner_wait.png"))
loadbtn=pygame.image.load(os.path.join(libzox.gfxpath, "loadbtn.png"))
loadbtn_inact=pygame.image.load(os.path.join(libzox.gfxpath, "loadbtn_inact.png"))

backbtn=pygame.image.load(os.path.join(libzox.gfxpath, "backbtn.png"))
backbtn_inact=pygame.image.load(os.path.join(libzox.gfxpath, "backbtn_inact.png"))
nextbtn=pygame.image.load(os.path.join(libzox.gfxpath, "nextbtn.png"))
nextbtn_inact=pygame.image.load(os.path.join(libzox.gfxpath, "nextbtn_inact.png"))
upbtn=pygame.image.load(os.path.join(libzox.gfxpath, "upbtn.png"))
upbtn_inact=pygame.image.load(os.path.join(libzox.gfxpath, "upbtn_inact.png"))
rootbtn=pygame.image.load(os.path.join(libzox.gfxpath, "rootbtn.png"))
rootbtn_inact=pygame.image.load(os.path.join(libzox.gfxpath, "rootbtn_inact.png"))
perrorbtn=pygame.image.load(os.path.join(libzox.gfxpath, "perrorbtn.png"))
perrorbtn_inact=pygame.image.load(os.path.join(libzox.gfxpath, "perrorbtn_inact.png"))




#common:
scrollup=pygame.image.load(os.path.join(libzox.gfxpath, "scrollu.png"))
scrolldn=pygame.image.load(os.path.join(libzox.gfxpath, "scrolld.png"))
scrollup_no=pygame.image.load(os.path.join(libzox.gfxpath, "scrollu_no.png"))
scrolldn_no=pygame.image.load(os.path.join(libzox.gfxpath, "scrolld_no.png"))

#bookmark window graphics
bookm_del0=pygame.image.load(os.path.join(libzox.gfxpath, "delinact.png"))
bookm_del1=pygame.image.load(os.path.join(libzox.gfxpath, "delact.png"))
bookm_go0=pygame.image.load(os.path.join(libzox.gfxpath, "goinact.png"))
bookm_go1=pygame.image.load(os.path.join(libzox.gfxpath, "goact.png"))
bookm_edit0=pygame.image.load(os.path.join(libzox.gfxpath, "editinact.png"))
bookm_edit1=pygame.image.load(os.path.join(libzox.gfxpath, "editact.png"))
bookm_newbm=pygame.image.load(os.path.join(libzox.gfxpath, "newbm.png"))
menucorner_book=pygame.image.load(os.path.join(libzox.gfxpath, "menucorner_book.png"))

go_wicon=pygame.image.load(os.path.join(libzox.gfxpath, "go_wicon.png"))
book_wicon=pygame.image.load(os.path.join(libzox.gfxpath, "book_wicon.png"))
bookedit_wicon=pygame.image.load(os.path.join(libzox.gfxpath, "bookedit_wicon.png"))
booknew_wicon=pygame.image.load(os.path.join(libzox.gfxpath, "booknew_wicon.png"))
more_wicon=pygame.image.load(os.path.join(libzox.gfxpath, "more_wicon.png"))
about_wicon=pygame.image.load(os.path.join(libzox.gfxpath, "about_wicon.png"))
help_wicon=pygame.image.load(os.path.join(libzox.gfxpath, "help_wicon.png"))

framesc=None

def init(framescape, desktop):
	global framesc
	global gtmenu
	global gtmenuremote
	global gtmenuint
	global gtmenuroot
	global gtmenurootremote
	global gthelp
	
	
	global gtimage
	global gttext
	global gtquery
	
	global gtsound
	global gtbin
	global gtweb
	global gterror
	global gtEND
	global gtTOP
	global highlight_arrow
	
	global deskt
	global loadingimage
	
	global media_play
	global media_stop
	global media_next
	global media_back
	global media_pause
	deskt=desktop
	framesc=framescape
	#load Gopher type icons.
	gthelp=pygame.image.load(os.path.join(libzox.gfxpath, "menuhelpicn.png")).convert()	
	gtmenu=pygame.image.load(os.path.join(libzox.gfxpath, "menuicn.png")).convert()
	gtmenuremote=pygame.image.load(os.path.join(libzox.gfxpath, "menuremoteicn.png")).convert()
	gtmenuint=pygame.image.load(os.path.join(libzox.gfxpath, "menuinticn.png")).convert()
	gtmenuroot=pygame.image.load(os.path.join(libzox.gfxpath, "menurooticn.png")).convert()
	gtmenurootremote=pygame.image.load(os.path.join(libzox.gfxpath, "menurootremoteicn.png")).convert()
	
	gtimage=pygame.image.load(os.path.join(libzox.gfxpath, "imageicon.png")).convert()
	gttext=pygame.image.load(os.path.join(libzox.gfxpath, "texticon.png")).convert()
	gtquery=pygame.image.load(os.path.join(libzox.gfxpath, "queryicon.png")).convert()
	
	gtsound=pygame.image.load(os.path.join(libzox.gfxpath, "soundicn.png")).convert()
	gtbin=pygame.image.load(os.path.join(libzox.gfxpath, "binicn.png")).convert()
	gtweb=pygame.image.load(os.path.join(libzox.gfxpath, "webicn.png")).convert()
	gterror=pygame.image.load(os.path.join(libzox.gfxpath, "erroricn.png")).convert()
	#special markers
	highlight_arrow=pygame.image.load(os.path.join(libzox.gfxpath, "highlight_arrow.png")).convert()
	gtEND=pygame.image.load(os.path.join(libzox.gfxpath, "eof_icon.png")).convert()
	gtTOP=pygame.image.load(os.path.join(libzox.gfxpath, "top_icon.png")).convert()

	loadingimage=pygame.image.load(os.path.join(libzox.gfxpath, "loadingimage.png")).convert()
	
	media_play=pygame.image.load(os.path.join(libzox.gfxpath, "media_play.png")).convert()
	media_pause=pygame.image.load(os.path.join(libzox.gfxpath, "media_pause.png")).convert()
	media_stop=pygame.image.load(os.path.join(libzox.gfxpath, "media_stop.png")).convert()
	media_next=pygame.image.load(os.path.join(libzox.gfxpath, "media_next.png")).convert()
	media_back=pygame.image.load(os.path.join(libzox.gfxpath, "media_back.png")).convert()
	






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
		self.taskrects={}
		self.tasksorted=[]
		self.mattesurf=None
		self.late_init=0
		self.prevactframe=None
		self.prevproclen=None
		self.actindex=None
		self.framecount=1
		self.frametime=15
		self.wmbuttonfont=pygame.font.SysFont(None, 22)
		
		return
	#def process(self):
	#	while self.active:
	#		self.clock.tick(1)
	#	print("done.")
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==0:
			
			if self.late_init==1:
				self.late_init=0
				self.drawdesk(frameobj.surface)
			else:
				if self.prevactframe!=framesc.activeframe or self.prevproclen!=len(framesc.proclist):
					self.prevactframe=framesc.activeframe
					self.prevproclen=len(framesc.proclist)
					self.drawdesk(frameobj.surface)
				if self.framecount==self.frametime:
					self.framecount=1
					self.drawdesk(frameobj.surface)
				else:
					self.framecount+=1
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
			if mpos[1]<50:
				for prog in self.progs:
					if prog.iconrect.collidepoint(mpos):
						self.hovertext=prog.hint
				for framex in self.taskrects:
					if self.taskrects[framex].collidepoint(mpos):
						self.hovertext=framex.name
				
				if self.mascotrect.collidepoint(mpos):
					self.hovertext="About Zoxenpher."
		#init code
		if frameobj.statflg==1:
			stz.setminy(51)
			self.late_init=1
			#self.drawdesk(frameobj.surface)
		#shutdown code
		if frameobj.statflg==3:
			print("shutting down...")
			#prevent new connections.
			libgop.stopget=2
			print("Stopping MPE...")
			MPE.shutdown()
			self.active=0
		if frameobj.statflg==4:
			if data.button==1:
				#about button
				if self.mascotrect.collidepoint(data.pos):
					newgop=gopherpane(host="zoxsplash>>", port=70, selector="/about.gop", shortprefix="About: ")
					framesc.add_frame(stz.framex(gopherwidth, gopherheight, "Gopher Menu", resizable=1, pumpcall=newgop.pumpcall1))
					abtzox=libzoxui.aboutsplash()
					framesc.add_frame(stz.framex(600, 150, "About Zoxenpher", resizable=0, pumpcall=abtzox.pumpcall1))
				#task switcher logic
				for framex in self.taskrects:
					if self.taskrects[framex].collidepoint(data.pos):
						framesc.raise_frame(framex)
				#launcher icons
				for prog in self.progs:
					if prog.iconrect.collidepoint(data.pos):
						framesc.add_frame(stz.framex(prog.xsize, prog.ysize, prog.friendly_name, pumpcall=prog.classref().pumpcall1, resizable=prog.resizable))
			elif data.button==4 and data.pos[1]<46:
				try:
					if len(self.tasksorted)>1:
						if self.actindex==None:
							framesc.raise_frame(self.tasksorted[0])
						elif self.actindex==0:
							framesc.raise_frame(self.tasksorted[-1])
						else:
							framesc.raise_frame(self.tasksorted[self.actindex-1])
				except IndexError:
					print("Index Error In back window cycle.")
			elif data.button==5 and data.pos[1]<46:
				try:
					if len(self.tasksorted)>1:
						if self.actindex==None:
							framesc.raise_frame(self.tasksorted[0])
						elif self.actindex==len(self.tasksorted)-1:
							framesc.raise_frame(self.tasksorted[0])
						else:
							framesc.raise_frame(self.tasksorted[self.actindex+1])
				except IndexError:
					print("Index Error In forward window cycle.")
			elif data.button in [4, 5]:
				self.drawdesk(frameobj.surface)
				
				
		#resize
		if frameobj.statflg==8:
			self.resize(frameobj.surface)
			#reset tile background
			self.mattesurf=None
			self.drawdesk(frameobj.surface)#Needed only if a resizable desk is desired.
		if frameobj.statflg==6:
			mods=pygame.key.get_mods()
			if data.key==pygame.K_TAB and mods & pygame.KMOD_CTRL:
				try:
					if len(self.tasksorted)>1:
						if self.actindex==None:
							framesc.raise_frame(self.tasksorted[0])
						elif self.actindex==len(self.tasksorted)-1:
							framesc.raise_frame(self.tasksorted[0])
						else:
							framesc.raise_frame(self.tasksorted[self.actindex+1])
				except IndexError:
					print("Index Error In forward window cycle.")
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
		self.mascot=pygame.image.load(os.path.join(libzox.gfxpath, "mascot45.png")).convert(surface)
		#self.iconend=pygame.image.load(os.path.join(libzox.gfxpath, "iconbarend.png")).convert(surface)
		#self.iconbegin=pygame.image.load(os.path.join(libzox.gfxpath, "iconbarbegin.png")).convert(surface)
		#QUESTION: why does .convert_alpha(surface) need display mode set, but .convert(surface) does not? this makes zero sense!
		self.zban=pygame.image.load(os.path.join(libzox.gfxpath, "zoxbanner.png"))
		self.resize(surface)
		if tiledraw!=None:
			self.tilesurf=tiledraw.convert(surface)
		else:
			self.tilesurf=None
		for prog in self.progs:
			prog.icon=prog.icon.convert(surface)
	##
	def drawdesk(self, surface):
		#Save CPU time by reseting auto-render timer. 
		#(avoids needlessly rendering the desktop via the timer when its triggered otherwise)
		self.framecount=1
		
		if not self.imgload:
			self.imgload=1
			self.imageloader(surface)
		surface.fill((208, 211, 224))
		if self.tilesurf!=None:
			if self.mattesurf==None:
				self.mattesurf=(libzox.tiledraw(surface, self.tilesurf, self.zban)).convert(surface)
			surface.blit(self.mattesurf, (0, 0))
			
			
			
		#surface.blit(self.wallpaperx, (0, 0))
		#surface.blit(self.mascot, (surface.get_width()//2-self.mascot.get_width()//2, surface.get_height()//2-self.mascot.get_height()//2))
		icnx=0
		icny=0
		icnxjmp=45
		icnyjmp=50
		pygame.draw.rect(surface, (220, 220, 220), pygame.Rect(0, 0, surface.get_width(), 45))
		pygame.draw.line(surface, (20, 40, 80), (0, 45), (surface.get_width(), 45), 1)
		for prog in self.progs:
			if not prog.side:
				prog.iconrect=surface.blit(prog.icon, (icnx, icny))
				icnx+=icnxjmp
		#surface.blit(self.iconend, (icnx, icny))
		#icnx+=icnxjmp//2
		
		#urllabel=simplefont.render(self.hovertext, True, (255, 255, 255), (60, 60, 120))
		urllabel=hudfont.render(self.hovertext, True, (0, 0, 0), (220, 220, 220))
		surface.blit(urllabel, (icnx+10, 0))
		#task switcher:
		self.taskrects={}
		icnx=icnx+1
		
					
		
		mascotx=surface.get_width()-self.mascot.get_width()
		self.mascotrect=surface.blit(self.mascot, (mascotx, 0))
		for prog in self.progs:
			if prog.side:
				mascotx-=45
				prog.iconrect=surface.blit(prog.icon, (mascotx, icny))
		#mascotx-=self.iconbegin.get_width()
		#surface.blit(self.iconbegin, (mascotx, 0))
		
		if framesc==None:
			self.late_init=1
		else:
			try:
				buttonsize=int(((mascotx-1)-icnx)/len(framesc.proclist))
			except ZeroDivisionError:
				buttonsize=25
			buttonrect=pygame.Rect(icnx, 19, buttonsize, 25)
			#sort the tasks via PID to keep task icons from "jumping"
			indx=0
			self.actindex=None
			self.tasksorted=sorted(framesc.proclist, key=lambda x: x.pid, reverse=False)
			for framex in self.tasksorted:
				if framex.shade:
					framename="="+framex.name+"="
				else:
					framename=framex.name
				if framex.wo==0:
					pygame.draw.rect(surface, (60, 60, 110), buttonrect, 0)
					#pygame.draw.rect(surface, (255, 255, 255), buttonrect, 1)
					self.actindex=indx
					nametx=self.wmbuttonfont.render(framename, True, (255, 255, 255), (60, 60, 110)).convert()
				else:
					pygame.draw.rect(surface, (160, 160, 160), buttonrect, 0)
					#pygame.draw.rect(surface, (0, 0, 0), buttonrect, 1)
					nametx=self.wmbuttonfont.render(framename, True, (255, 255, 255), (160, 160, 160)).convert()
				indx+=1
				if framex.icon!=None:
					frect=surface.blit(framex.icon, (buttonrect.x, 19))
					#icnx+=framex.icon.get_width()
					self.taskrects[framex]=buttonrect.copy()
				else:
					frect=surface.blit(gterror, (buttonrect.x, 19))
					#icnx+=gterror.get_width()
					self.taskrects[framex]=buttonrect.copy()
				nametxrect=nametx.get_rect()
				if nametxrect.w>buttonsize-25-6:
					nametxrect.w=buttonsize-25-6
				surface.blit(nametx, (buttonrect.x+29, 21), area=nametxrect)
				buttonrect.x+=buttonsize
				







#text document wrapper for gopherpane
def textshow(host, port, selector):
	data=pathfigure(host, port, selector, gtype="0")
	menu=libgop.menudecode(data, txtflg=1)
	newgop=gopherpane(host=host, port=port, selector=selector, preload=menu, prefix="text: gopher://", gtype="0", shortprefix="text: ")
	framesc.add_frame(stz.framex(gopherwidth, gopherheight, "Text Document", resizable=1, pumpcall=newgop.pumpcall1, xpos=20))



#gopher menu class. also used for text documents
class gopherpane:
	def __init__(self, host='zoxsplash>>', port=70, selector="/", prefix="menu: gopher://", preload=None, forceimage=0, linkdisable=0, gtype="1", shortprefix="menu: ", loading=1, query=None):
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
		self.perrorbtn=perrorbtn.convert()
		self.perrorbtn_inact=perrorbtn_inact.convert()
		self.loading=loading
		self.prevtype=None
		self.PageError=0
		self.ServError=0
		self.query=query
		self.PageErrorList=[]
	#menu get routine
	def menuget(self):
		
		if self.gtype=="0":
			txtflg=1
		else:
			txtflg=0
		self.data=pathfigure(self.host, self.port, self.selector, self.gtype, self.query)
		self.menu=libzox.SecureFilter(libgop.menudecode(self.data, txtflg=txtflg), self.host)
		for item in self.renderdict:
			del item
		del self.renderdict
		#print("newhist")
		self.renderdict={}
		self.histlist=self.histlist[:self.histpoint+1]
		self.histlist.extend([libzox.histitem(self.host, self.port, self.selector, self.gtype, self.data, self.menu, self.query)])
		self.histpoint+=1
		if len(self.histlist)==histsize+1:
			#print("histpop")
			self.histlist.pop(0)
			self.histpoint-=1
	def menuget_nohist(self):
		
		if self.gtype=="0":
			txtflg=1
		else:
			txtflg=0
		self.data=pathfigure(self.host, self.port, self.selector, self.gtype, self.query)
		self.menu=libzox.SecureFilter(libgop.menudecode(self.data, txtflg=txtflg), self.host)
		for item in self.renderdict:
			del item
		del self.renderdict
		self.renderdict={}
	def newhist(self):
		#print("newhist")
		self.histlist=self.histlist[:self.histpoint+1]
		self.histlist.extend([libzox.histitem(self.host, self.port, self.selector, self.gtype, self.data, self.menu, self.query)])
		self.histpoint+=1
		if len(self.histlist)==histsize+1:
			#print("histpop")
			self.histlist.pop(0)
			self.histpoint-=1
	
	#check code for whether to draw a black arrow next to an informational type.
	#attempts to identify section dividers and section-dividing titles.
	#i.e.
	#-----------------------
	#--------Example title-------
	def highlight_check(self, itemname):
		if itemname.startswith("--") and itemname.endswith("--"):
			return 1
		if itemname.startswith("__") and itemname.endswith("__"):
			return 1
		if itemname.startswith("==") and itemname.endswith("=="):
			return 1
		if itemname.startswith("**") and itemname.endswith("**"):
			return 1
		return 0
	#render routine
	def menudraw(self, frameobj):
		imageset=[]
		imagecount=0
		self.ypos=self.yoff
		
		surfhig=frameobj.surface.get_height()
		surfwid=frameobj.surface.get_width()

		frameobj.surface.fill((255, 255, 255))
		self.siderect=pygame.Rect(0, 0, 25, surfhig)
		#pygame.draw.rect(frameobj.surface, (185, 195, 255), self.siderect)
		pygame.draw.rect(frameobj.surface, (223, 223, 223), self.siderect)
		pygame.draw.line(frameobj.surface, (0, 0, 0), (25, 0), (25, surfhig), 1)
		count=0
		#"lead in" code
		self.ypos+=2
		if self.ypos>=0:
			frameobj.surface.blit(gtTOP, (0, self.ypos))
			leadrect=pygame.Rect(26, 0, surfwid, self.ypos)
			pygame.draw.rect(frameobj.surface, (107, 107, 107), leadrect)
			pygame.draw.line(frameobj.surface, (0, 0, 0), (25, self.ypos), (surfwid-4, self.ypos), 1)
		
		
		
		# "document edge" code
		docsiderect=pygame.Rect(surfwid-4, 0, 4, surfhig)
		pygame.draw.rect(frameobj.surface, (107, 107, 107), docsiderect)
		if self.ypos>=0:
			pygame.draw.line(frameobj.surface, (0, 0, 0), (surfwid-4, self.ypos), (surfwid-4, surfhig), 1)
		else:
			pygame.draw.line(frameobj.surface, (0, 0, 0), (surfwid-4, 0), (surfwid-4, surfhig), 1)
		#gtTOP offset needs to be added here, for docuemnt edge lines to add up.
		self.ypos+=6
		
		
		for item in self.menu:
			if item.gtype=="3":
				self.ServError+=1
				rects, self.ypos, self.renderdict = textitem(item.name, simplefont, self.yjump, (155, 0, 0), frameobj.surface, self.ypos, self.renderdict, gterror)
			elif item.gtype=="i":
				if item.gtype=="0":
					rects, self.ypos, self.renderdict = textitem(item.name, simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.ypos, self.renderdict)
				elif self.highlight_check(item.name):
					rects, self.ypos, self.renderdict = textitem(item.name, simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.ypos, self.renderdict, highlight_arrow, iconsize=5)
				else:
					rects, self.ypos, self.renderdict = textitem(item.name, simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.ypos, self.renderdict)

				
				
			#If text, show unformatted lines
			elif item.gtype==None and (self.gtype=="0"):
				rects, self.ypos, self.renderdict = textitem(item.name, simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.ypos, self.renderdict)
			#if not text, then gtype==None means an error. this code displays red error text, and, upon seeing an error for the first time, adds that selector to the PageErrorList
			elif item.gtype==None:
				rects, self.ypos, self.renderdict = textitem("[" + item.errorlabel + "]: " + item.errorinfo + " DEBUG: ''" + item.debug + "''", simplefont, self.yjump, (155, 0, 0), frameobj.surface, self.ypos, self.renderdict)
				if item not in self.PageErrorList:
					print(item.errorlabel + ": Line: " + str(count) + ", in document '" + str(self.selector) + "'\n   from server: '" + str(self.host) + ":" + str(self.port) + "'\n  ERROR INFO: ''" + item.errorinfo + "'\n  DEBUG: ''" + item.debug + "''")
					self.PageError+=1
					self.PageErrorList.extend([item])
			#END OF FILE dot
			elif item.gtype=="END":
				#rect, self.ypos, self.renderdict = textitem("", linkfont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtEND, 1)
				pass
			elif item.gtype=="1" and item.hostname=="zoxhelp>>":
				rect, self.ypos, self.renderdict = textitem(item.name, linkfont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gthelp, 1)
				item.rect=rect
			#TODO: add seprate gtmenufile icon for file directories. if anything like downloads>> or usr>> is added, they should also use gtmenufile.
			elif item.gtype=="1" and (item.hostname=="zox>>" or item.hostname=="zoxsplash>>" or item.hostname=="file>>"):
				rect, self.ypos, self.renderdict = textitem(item.name, linkfont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtmenuint, 1)
				item.rect=rect
			elif item.gtype=="1" and item.hostname!=self.host and (item.selector=="/" or item.selector==""):
				rect, self.ypos, self.renderdict = textitem(item.name, linkfont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtmenurootremote, 1)
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
				#check to see if image is loaded, if not, add it to image preview queue (if preview cap is not met yet/rendering local documentation.)
				#place a placeholder "loading" image to be shown until image has loaded.
				try:
					foobar=item.image
					
				except AttributeError as err:
					#print(err)
					if imagecount<maximages or (imagecount<2 and self.forceimage) or libzox.isinternalhost(self.host):
						item.image=loadingimage.copy()
						item.fullimage=None
						imageset.extend([item])
					else:
						item.image=None
						item.fullimage=None
					#item.rect, self.ypos, self.renderdict = textitem(item.name, simplefont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtimage, 1)

				if item.image!=None:
					ytemp=0
					if item.name.strip()!="":
						rectia, self.ypos, self.renderdict = textitem(item.name, simplefont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtimage, 1)
					else:
						rectia, ytemp, self.renderdict = textitem(item.name, simplefont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtimage, 1)
					rectib=frameobj.surface.blit(item.image, (26, self.ypos))
					item.rect=rectia.unionall([rectib])
					#pygame.draw.rect(frameobj.surface, (60, 60, 255), item.rect, 1)
					itemimagehig=item.image.get_height()
					if ytemp!=0:
						lsize=abs(ytemp-self.ypos)
						if lsize<itemimagehig:
							lsize=itemimagehig
						self.ypos+=lsize
					else:	
						self.ypos+=itemimagehig
				if item.image==None:
					item.rect, self.ypos, self.renderdict = textitem(item.name, simplefont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, gtimage, 1)
				#pygame.draw.rect(frameobj.surface, (255, 255, 0), item.rect, 1)
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
			count+=1
		#launch image loader thread if needed
		if imageset!=[]:
			self.images=imageset
			self.loading=1
			sideproc=Thread(target = imgget, args = [imageset, self.menudraw, frameobj, self])
			sideproc.daemon=True
			sideproc.start()
		
		if self.ypos<surfhig:
			frameobj.surface.blit(gtEND, (0, self.ypos))
			endrect=pygame.Rect(26, self.ypos, surfwid, surfhig-self.ypos)
			endrect_shadow=pygame.Rect(26, self.ypos, surfwid-49, 20)
			pygame.draw.rect(frameobj.surface, (107, 107, 107), endrect)
			pygame.draw.rect(frameobj.surface, (47, 47, 47), endrect_shadow)
			pygame.draw.line(frameobj.surface, (0, 0, 0), (25, self.ypos), (surfwid-4, self.ypos), 1)
		self.ypos+=25
		
		self.hudrect=pygame.Rect(0, 0, frameobj.surface.get_width(), 22)
		pygame.draw.rect(frameobj.surface, (220, 220, 220), self.hudrect)
		#self.hudcorner=pygame.Rect(0, 0, 25, 22)
		#pygame.draw.rect(frameobj.surface, (255, 255, 255), self.hudcorner)
		if self.loading:
			frameobj.surface.blit(self.menucorner_wait, (0, 0))
		else:
			frameobj.surface.blit(self.menucorner, (0, 0))
		xpos=25
		if self.histpoint>0 and self.loading==0:
			self.backrect=frameobj.surface.blit(self.backbtn, (xpos, 0))
		else:
			self.backrect=frameobj.surface.blit(self.backbtn_inact, (xpos, 0))
		xpos+=60
		if self.histpoint<len(self.histlist)-1 and self.loading==0:
			self.nextrect=frameobj.surface.blit(self.nextbtn, (xpos, 0))
		else:
			self.nextrect=frameobj.surface.blit(self.nextbtn_inact, (xpos, 0))
		xpos+=60
		if "/" in self.selector and self.selector!="/":
			self.uprect=frameobj.surface.blit(self.upbtn, (xpos, 0))
		else:
			self.uprect=frameobj.surface.blit(self.upbtn_inact, (xpos, 0))
		xpos+=60
		if self.selector!="/" and self.selector!="":
			self.rootrect=frameobj.surface.blit(self.rootbtn, (xpos, 0))
		else:
			self.rootrect=frameobj.surface.blit(self.rootbtn_inact, (xpos, 0))
		xpos+=60
		#pygame.draw.line(frameobj.surface, (255, 255, 255), (xpos, 0), (xpos, 25), 0)
		xpos+=8
		self.bookrect=frameobj.surface.blit(self.bookbtn, (xpos, 0))
		xpos+=60
		if self.loading:
			self.loadrect=frameobj.surface.blit(self.loadbtn_inact, (xpos, 0))
		else:
			self.loadrect=frameobj.surface.blit(self.loadbtn, (xpos, 0))
		xpos+=60
		if self.PageError!=0 or self.ServError!=0:
			self.erroriconRect=frameobj.surface.blit(self.perrorbtn, (xpos, 0))
		else:
			self.erroriconRect=frameobj.surface.blit(self.perrorbtn_inact, (xpos, 0))
		
		if self.yoff<25:
			self.scuprect=frameobj.surface.blit(self.scrollup, (frameobj.surface.get_width()-24, 0))
		else:
			self.scuprect=frameobj.surface.blit(self.scrollup_no, (frameobj.surface.get_width()-24, 0))
		if self.ypos>frameobj.sizey:
			self.scdnrect=frameobj.surface.blit(self.scrolldn, (frameobj.surface.get_width()-46, 0))
		else:
			self.scdnrect=frameobj.surface.blit(self.scrolldn_no, (frameobj.surface.get_width()-46, 0))
		
	#menu change loader
	def menuchange(self, item, frameobj):
		self.host=item.hostname
		self.port=item.port
		self.selector=item.selector
		self.query=None
		self.menuget()
		self.set_icon_name(frameobj)
		
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
		#reset page error flag-counter
		self.PageError=0
		#reset server error flag-counter
		self.ServError=0
		self.PageErrorList=[]
		
		self.yoff=25
		self.loading=0
		self.menudraw(frameobj)
	def menuroot(self, frameobj):
		self.selector="/"
		self.gtype="1"
		self.query=None
		#reset prefixes in case of text document being the current.
		self.menuget()
		self.set_icon_name(frameobj)
		
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
		self.query=None
		#reset prefixes in case of text document being the current.
		self.menuget()
		self.set_icon_name(frameobj)
		
		self.yoff=25
		self.loading=0
		self.menudraw(frameobj)
	#menu initalization loader
	def menuinital(self, frameobj):
		
		self.menuget()
		self.set_icon_name(frameobj)
		
		
		self.yoff=25
		self.loading=0
		self.menudraw(frameobj)
	def histchange(self, histitem, frameobj):
		self.data=histitem.data
		self.menu=histitem.menu
		self.host=histitem.host
		self.port=histitem.port
		self.query=histitem.query
		self.selector=histitem.selector
		self.gtype=histitem.gtype
		self.set_icon_name(frameobj)
		
		self.renderdict={}
		self.yoff=25
		self.menudraw(frameobj)
	def set_icon_name(self, frameobj):
		#reset page error flag-counter
		self.PageError=0
		#reset server error flag-counter
		self.ServError=0
		self.PageErrorList=[]
		if self.host=="zoxsplash>>" and self.selector=="/about.gop":
			self.prefix="about: "
			self.shortprefix="about: "
			frameobj.seticon(about_wicon.convert())
		elif self.host=="zoxhelp>>":
			self.prefix="help: "
			self.shortprefix="help: "
			frameobj.seticon(help_wicon.convert())
		elif self.host=="zoxsplash>>":
			self.prefix="Splash: "
			self.shortprefix="Splash: "
			frameobj.seticon(gtmenuint)
		elif self.host=="zox>>":
			self.prefix="about: "
			self.shortprefix="about: "
			frameobj.seticon(gtmenuint)
		elif self.host=="file>>":
			self.prefix="file: "
			self.shortprefix="file: "
			#TODO: add special gtmenufile icon here. note that anything like usr>> or downloads>> should share this icon.
			frameobj.seticon(gtmenuint)
		elif self.gtype=="0":
			self.prefix="text: gopher://"
			self.shortprefix="text: "
			frameobj.seticon(gttext)
		elif self.gtype=="7":
			self.prefix="query: gopher://"
			self.shortprefix="query: "
			frameobj.seticon(gtquery)
		else:
			self.prefix="menu: gopher://"
			self.shortprefix="menu: "
			if self.selector=="/" or self.selector=="":
				frameobj.seticon(gtmenuroot)
			else:
				frameobj.seticon(gtmenu)
		if self.query!=None:
			querystring=" ?:" + self.query
		else:
			querystring=""
		if self.host=="zoxsplash>>" and self.selector=="/about.gop":
			frameobj.name="About Zoxenpher"
		elif self.host=="zoxhelp>>":
			try:
				frameobj.name="Help: "+self.menu[0].name
			except IndexError:
				frameobj.name="Help"
		elif self.host in ["zox>>", "zoxsplash>>"]:
			frameobj.name=(self.shortprefix+str(self.selector))
		else:
			frameobj.name=(self.prefix+str(self.host) + "/" + self.gtype + str(self.selector) + querystring)
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
			elif self.erroriconRect.collidepoint(mpos):
				if self.PageError!=0 and self.ServError!=0:
					deskt.hovertext=str(self.ServError) + " Server Error(s). " + str(self.PageError) + " Page Error(s)."
				elif self.PageError!=0:
					deskt.hovertext=str(self.PageError) + " Page Error(s)."
				elif self.ServError!=0:
					deskt.hovertext=str(self.ServError) + " Server Error(s)."
				else:
					deskt.hovertext="No Errors detected."
			#link-url on mouseover code
			elif not self.hudrect.collidepoint(mpos):
				for item in self.menu:
					if item.gtype!=None:
						#normal (supported) gopher types
						if item.gtype in "01pgI7s":
							try:
								if item.rect.collidepoint(mpos):
									if libzox.isinternalhost(item.hostname):
										deskt.hovertext=(item.hostname + "/" + item.gtype + item.selector)
									else:
										deskt.hovertext=("gopher://" + item.hostname + "/" + item.gtype + item.selector)
									break
							except AttributeError:
								continue
						#web url
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
			del self.histlist
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
			
			if data.key==pygame.K_m:
				newgop=bookmadded(url=libzox.gurlencode(self.host, self.selector, self.gtype, self.port, self.query))
				framesc.add_frame(stz.framex(500, 150, "New Bookmark", resizable=1, pumpcall=newgop.pumpcall1, sizeminy=150))
			#home/end functionality.
			if data.key==pygame.K_HOME:
				self.yoff=25
				self.menudraw(frameobj)
			if data.key==pygame.K_END:
				if self.ypos>frameobj.sizey:
					self.yoff=-abs((self.ypos+abs(self.yoff))-frameobj.sizey)
					self.menudraw(frameobj)
			
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
			else:
				if data.key==pygame.K_UP:
					self.yoff+=self.yjump*2
					if self.yoff>25:
						self.yoff=25
					self.menudraw(frameobj)
				if data.key==pygame.K_DOWN and self.ypos>frameobj.sizey:
					self.yoff-=self.yjump*2
					self.menudraw(frameobj)
			if data.key==pygame.K_PAGEUP:
				self.yoff+=self.yjump*8
				if self.yoff>25:
					self.yoff=25
				self.menudraw(frameobj)
			if data.key==pygame.K_PAGEDOWN and self.ypos>frameobj.sizey:
				self.yoff-=self.yjump*8
				self.menudraw(frameobj)
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
						newgop=bookmadded(url=libzox.gurlencode(self.host, self.selector, self.gtype, self.port, self.query))
						framesc.add_frame(stz.framex(500, 150, "New Bookmark", resizable=1, pumpcall=newgop.pumpcall1,  sizeminy=150))
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
									framesc.add_frame(stz.framex(500, 150, "New Bookmark", resizable=1, pumpcall=newgop.pumpcall1, sizeminy=150))

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
								framesc.add_frame(stz.framex(500, 400, "Image", resizable=1, pumpcall=newgop.pumpcall1))
						if item.gtype=="7":
							if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
								newgop=querypane(host=item.hostname, port=item.port, selector=item.selector, itmdesc=item.name)
								framesc.add_frame(stz.framex(500, 100, "Gopher Query", resizable=1, pumpcall=newgop.pumpcall1, sizeminy=100))
						if item.gtype=="s":
							if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
								newgop=sndplay(item.hostname, item.port, item.selector)
								framesc.add_frame(stz.framex(500, 100, "Sound", resizable=1, pumpcall=newgop.pumpcall1, sizeminy=100))
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
			else:
				mods=pygame.key.get_mods()
				if mods & pygame.KMOD_SHIFT:
					if data.button==4:
						self.yoff+=self.yjump*8
						if self.yoff>25:
							self.yoff=25
						self.menudraw(frameobj)
					elif data.button==5 and self.ypos>frameobj.sizey:
						self.yoff-=self.yjump*8
						self.menudraw(frameobj)
				else:
					if data.button==4:
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
	def __init__(self, host, port, selector, query="", itmdesc=""):
		self.host=host
		self.port=port
		self.selector=selector
		self.yoff=0
		if itmdesc!="":
			self.querylabel="Query: "+itmdesc
		else:
			self.querylabel="Query: "+ self.host+"/7"+self.selector
		#self.hovmsg="Enter your query into the serarch box"
		self.yjump=int(libzox.cnfdict["menutextjump"])+2
		self.stringblob=query
		if self.stringblob==None:
			self.stringblob=""
		if self.host=="QUERYTEST":
			self.debug=1
		else:
			self.debug=0
		self.validchars='''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890,./<>?;':"[]{}-=_+)(*&^%$#@!`~\\|'''
	def renderdisp(self, frameobj):
		str1=self.host+"/7"+self.selector
		frameobj.surface.fill((220, 220, 220))
		#URL
		self.ypos=0
		pygame.draw.rect(frameobj.surface, (0, 0, 100), pygame.Rect(0, 0, frameobj.sizex, self.yjump+3))
		foo, self.ypos, bar = textitem(str1, simplefont, self.yjump, (255, 255, 255), frameobj.surface, self.ypos, {}, xoff=0, textcoly=(0, 0, 100))
		self.ypos+=3
		#QUERY LABEL
		foo, self.ypos, bar = textitem(self.querylabel, simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.ypos, {}, xoff=0, textcoly=(220, 220, 220))
		#TEXTBOX
		pygame.draw.rect(frameobj.surface, (255, 255, 255), pygame.Rect(2, self.ypos, frameobj.sizex-4, self.yjump*2+6))
		pygame.draw.rect(frameobj.surface, (0, 0, 0), pygame.Rect(2, self.ypos, frameobj.sizex-4, self.yjump*2+6), 1)
		foo, self.ypos, bar = textitem(self.stringblob+"|", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.ypos+3, {}, xoff=5)
	def loader(self, frameobj):
		frameobj.name="Loading..."
		#try:
		#	data=libgop.gopherget(self.host, self.port, self.selector, query=self.stringblob)
		#except Exception as err:
		#	print(err)
		#	data=open(os.path.join("vgop", "gaierror"))
		#menu=libgop.menudecode(data)
		newgop=gopherpane(host=self.host, port=self.port, selector=self.selector, gtype="7", query=self.stringblob)
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
			#str1=self.host+"/7"+self.selector
			#print("querypane:")
			#print(str1)
			#frameobj.name="query: "+str1
			frameobj.name=self.querylabel
			self.renderdisp(frameobj)
			frameobj.seticon(gtquery)
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
		pygame.draw.rect(frameobj.surface, (220, 220, 220), pygame.Rect(0, 0, frameobj.surface.get_width(), 22))
		frameobj.surface.blit(self.menucorner_book, (0, 0))
		self.newrect=frameobj.surface.blit(self.newbm, (205, 0))
		if self.funct==0:
			self.gorect=frameobj.surface.blit(self.go1, (25, 0))
			self.delrect=frameobj.surface.blit(self.del0, (85, 0))
			self.editrect=frameobj.surface.blit(self.edit0, (145, 0))
		elif self.funct==1:
			self.gorect=frameobj.surface.blit(self.go0, (25, 0))
			self.delrect=frameobj.surface.blit(self.del1, (85, 0))
			self.editrect=frameobj.surface.blit(self.edit0, (145, 0))
		else:
			self.gorect=frameobj.surface.blit(self.go0, (25, 0))
			self.delrect=frameobj.surface.blit(self.del0, (85, 0))
			self.editrect=frameobj.surface.blit(self.edit1, (145, 0))
		self.ypos=25
		for item in xlist:
			item.rect, self.ypos, self.renderdict = textitem(item.name, linkfont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict, itemicn=self.getitemtypeicn(item.url), link=1)
			#pygame.draw.line(frameobj.surface, (0, 0, 0), (26, self.ypos-1), (frameobj.sizex, self.ypos-1), 1)
			if libzox.itemdebug:
				try:
					pygame.draw.rect(frameobj.surface, (255, 0, 0), item.rect, 1)
				except AttributeError:
					pass
		if self.offset>0:
			self.scuprect=frameobj.surface.blit(self.scrollup, (frameobj.surface.get_width()-24, 0))
		else:
			self.scuprect=frameobj.surface.blit(self.scrollup_no, (frameobj.surface.get_width()-24, 0))
		if self.ypos>frameobj.sizey:
			self.scdnrect=frameobj.surface.blit(self.scrolldn, (frameobj.surface.get_width()-46, 0))
		else:
			self.scdnrect=frameobj.surface.blit(self.scrolldn_no, (frameobj.surface.get_width()-46, 0))
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
	def rotarylaunch(self, url, frameobj, itemname):
		self.host, self.port, self.selector, self.gtype, self.query = libzox.gurldecode(url)
		if self.gtype=="1":
			sideproc=Thread(target = self.loaderg1, args = [frameobj])
			sideproc.daemon=True
			sideproc.start()
		elif self.gtype=="0":
			sideproc=Thread(target = self.loaderg0, args = [frameobj])
			sideproc.daemon=True
			sideproc.start()
		elif self.gtype=="7":
			newgop=querypane(host=self.host, port=self.port, selector=self.selector, query=self.query, itmdesc="[book] "+itemname)
			framesc.add_frame(stz.framex(500, 100, "Gopher Query", resizable=1, pumpcall=newgop.pumpcall1, sizeminy=100))
		elif self.gtype=="g" or self.gtype=="p" or self.gtype=="I":
			newgop=imgview(host=self.host, port=self.port, selector=self.selector, gtype=self.gtype)
			framesc.add_frame(stz.framex(500, 400, "Image", resizable=1, pumpcall=newgop.pumpcall1))
		elif self.gtype=="s":
			newgop=sndplay(self.host, self.port, self.selector)
			framesc.add_frame(stz.framex(500, 100, "Sound", resizable=1, pumpcall=newgop.pumpcall1, sizeminy=100))
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
					if libzox.isinternalurl(item.url):
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
			frameobj.seticon(book_wicon.convert())
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
					framesc.add_frame(stz.framex(500, 150, "New Bookmark", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50, sizeminy=150))
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
							self.rotarylaunch(item.url, frameobj, item.name)
						if self.funct==1:
							libzoxui.do_yndialog("Delete Bookmark? (" + item.name + ")", "name: " + item.name + "\ngopher://" + item.url, self.deldiagret, canclose=1, carrydata=item)
						if self.funct==2:
							newgop=bookmadded(bookm=item)
							framesc.add_frame(stz.framex(500, 150, "Edit Bookmark", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50, sizeminy=150))
		



#bookmark creator/editor dialog.
class bookmadded:
	def __init__(self, url="", bookm=None, name=""):
		self.yoff=0
		self.yjump=int(libzox.cnfdict["menutextjump"])+2
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
		
		frameobj.surface.fill((220, 220, 220))
		#MESSAGE
		self.ypos=0
		pygame.draw.rect(frameobj.surface, (0, 0, 100), pygame.Rect(0, 0, frameobj.sizex, self.yjump+3))
		foo, self.ypos, bar = textitem("tab=switch textboxes, enter=accept", simplefont, self.yjump, (255, 255, 255), frameobj.surface, self.ypos, {}, xoff=0, textcoly=(0, 0, 100))
		self.ypos+=3+self.yjump
		#textitem("tab=switch entries, enter=accept", simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.yjump*1, {}, xoff=0)
		
		
		#if self.line:
			#textitem("gopher://"+self.urlblob+"", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*3, {}, xoff=0)
			#textitem("name:"+self.nameblob+"|", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*5, {}, xoff=0)
		#else:
			#textitem("gopher://"+self.urlblob+"|", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*3, {}, xoff=0)
			#textitem("name:"+self.nameblob+"", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*5, {}, xoff=0)
		if self.line:
			urlstr="gopher://"+self.urlblob+""
			namestr="name:"+self.nameblob+"|"
			urlcolor=(180, 180, 180)
			namecolor=(255, 255, 255)
		else:
			urlstr="gopher://"+self.urlblob+"|"
			namestr="name:"+self.nameblob+""
			urlcolor=(255, 255, 255)
			namecolor=(180, 180, 180)
		self.urlrect=pygame.Rect(2, self.ypos, frameobj.sizex-4, self.yjump*2+6)
		pygame.draw.rect(frameobj.surface, urlcolor, self.urlrect)
		pygame.draw.rect(frameobj.surface, (0, 0, 0), self.urlrect, 1)
		foo, self.ypos, bar = textitem(urlstr, simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.ypos+3, {}, xoff=5, textcoly=urlcolor)
		self.ypos+=self.yjump+12
		self.namerect=pygame.Rect(2, self.ypos, frameobj.sizex-4, self.yjump*2+6)
		pygame.draw.rect(frameobj.surface, namecolor, self.namerect)
		pygame.draw.rect(frameobj.surface, (0, 0, 0), self.namerect, 1)
		foo, self.ypos, bar = textitem(namestr, simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.ypos+3, {}, xoff=5, textcoly=namecolor)
		
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==2:
			self.renderdisp(frameobj)
		if frameobj.statflg==1:
			if self.bookm==None:
				frameobj.name="New Bookmark: " + self.url
				frameobj.seticon(booknew_wicon.convert())
			else:
				frameobj.name="Edit Bookmark: "
				frameobj.seticon(bookedit_wicon.convert())
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
		self.yjump=int(libzox.cnfdict["menutextjump"])+2
		self.stringblob=""
		#self.hovmsg="Enter a gopher URL to load."
		self.validchars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890:/.-_>"
	def renderdisp(self, frameobj):
		#frameobj.surface.fill((255, 255, 255))
		frameobj.surface.fill((220, 220, 220))
		#MESSAGE
		self.ypos=0
		pygame.draw.rect(frameobj.surface, (0, 0, 100), pygame.Rect(0, 0, frameobj.sizex, self.yjump+3))
		foo, self.ypos, bar = textitem("Please Type URL", simplefont, self.yjump, (255, 255, 255), frameobj.surface, self.ypos, {}, xoff=0, textcoly=(0, 0, 100))
		self.ypos+=3+self.yjump
		pygame.draw.rect(frameobj.surface, (255, 255, 255), pygame.Rect(2, self.ypos, frameobj.sizex-4, self.yjump*2+6))
		pygame.draw.rect(frameobj.surface, (0, 0, 0), pygame.Rect(2, self.ypos, frameobj.sizex-4, self.yjump*2+6), 1)
		foo, self.ypos, bar = textitem("gopher://"+self.stringblob+"|", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.ypos+3, {}, xoff=5)

		#textitem("Please Type URL", simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.yjump*2, {}, xoff=0)
		#textitem("gopher://"+self.stringblob+"|", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*4, {}, xoff=0)
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
			frameobj.sizeminy=100
			frameobj.name="URL GO:"
			frameobj.seticon(go_wicon.convert())
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
						framesc.add_frame(stz.framex(500, 100, "Gopher Query", resizable=1, pumpcall=newgop.pumpcall1, sizeminy=100))
						framesc.close_pid(frameobj.pid)
					elif self.gtype=="s":
						newgop=sndplay(self.host, self.port, self.selector)
						framesc.add_frame(stz.framex(500, 100, "Sound", resizable=1, pumpcall=newgop.pumpcall1, sizeminy=100))
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
		self.dummysurf=pygame.image.load(os.path.join(libzox.gfxpath, "loadingimage.png"))
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
			self.surf=pygame.image.load(os.path.join(libzox.gfxpath, "giaerror.png"))
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
			frameobj.seticon(gtimage)
			if libzox.isinternalhost(self.host):
				frameobj.name=("Image: " + str(self.host) + "/" + self.gtype + self.selector)
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
				framesc.add_frame(stz.framex(500, 150, "New Bookmark", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50, sizeminy=150))
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
			frameobj.seticon(gtsound)
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
				
				

class MediaPlaybackEngine:
	def __init__(self):
		self.playlist=[]
		self.playing=0
		self.repeatmode=0
		self.trackindex=None
		#if set to 1, MPE should wait in a loop for the current
		#self.trackindex to load, then play it.
		self.loadtrack=0
		#if not none, the given track should be added and played (the latter if its loaded yet)
		self.tracktoadd=None
		#if not none, the given track should be removed, and if playing, stopped, and self.trackindex be reset to 0)
		self.tracktoremove=None
		self.run=1
		self.shutdown_ready=0
	def Process(self):
		print("Zoxenpher Media Playback Engine initialized.")
		while self.run:
			time.sleep(0.1)
		self.shutdown_ready=1
	#blocking shutdown mechanism.
	def shutdown(self):
		self.run=0
		while not self.shutdown_ready:
			time.sleep(0.1)
	def AddPlay(self, song):
		if song not in self.playlist:
			self.tracktoadd=song
	def RemoveStop(self, song):
		if song in self.playlist:
			self.tracktoremove=song
			


##MEDIA PLAYBACK ENGINE STARTUP
print("Start MPE...")
MPE=MediaPlaybackEngine()
sideproc=Thread(target = MPE.Process)
sideproc.daemon=True
sideproc.start()


class Song:
	def __init__(self, host, port, selector, nametext=None):
		if selector.lower().endswith(".mp3"):
			self.mtype="MP3 Audio"
		elif selector.lower().endswith(".ogg"):
			self.mtype="OGG Audio"
		elif selector.lower().endswith(".wav"):
			self.mtype="Wave Audio"
		elif selector.lower().endswith(".midi"):
			self.mtype="MIDI"
		elif selector.lower().endswith(".mod"):
			self.mtype="MIDI"
		else:
			self.mtype="Unknown"
		
		self.host=host
		self.port=port
		self.slector=selector
		self.ready=0
		self.loading=1
		self.nametext=nametext
		if self.nametext==None:
			self.nametext=host+"/s"+selector
		self.data=None
		self.sound=None
		sideproc=Thread(target = self.loadaudio)
		sideproc.daemon=True
		sideproc.start()
	def loadaudio(self):
		self.data=pathfigure(self.host, self.port, self.selector, gtype='s')
		
		if self.data!=None and self.data!=0:
			self.ready=1
			self.loading=0
		elif self.data==None:
			self.error=1
			self.ready=0
			self.loading=0



class mediaplay:
	def __init__(self):
		self.yoff=0
		self.yjump=int(libzox.cnfdict["menutextjump"])
		self.data=0
		self.buttonbarsize=20+(45*5)
	def renderdisp(self, frameobj):
		frameobj.surface.fill((100, 100, 100))
		boff=(frameobj.surface.get_width()//2)-(self.buttonbarsize//2)
		self.hudrect=pygame.Rect(0, 0, frameobj.sizex, 45)
		pygame.draw.rect(frameobj.surface, (220, 220, 220), self.hudrect)
		self.playrect=frameobj.surface.blit(media_play, (0+boff, 0))
		self.pauserect=frameobj.surface.blit(media_pause, (45+boff, 0))
		
		self.backrect=frameobj.surface.blit(media_back, (110+boff, 0))
		self.stoprect=frameobj.surface.blit(media_stop, (155+boff, 0))
		self.nextrect=frameobj.surface.blit(media_next, (200+boff, 0))
		
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==2:
			self.renderdisp(frameobj)
		if frameobj.statflg==1:
			frameobj.name="Zoxenpher Media Player"
			self.renderdisp(frameobj)
			#sideproc=Thread(target = self.loader, args = [frameobj])
			#sideproc.daemon=True
			#sideproc.start()
			frameobj.seticon(gtsound)
				
				
##### mtype key:
#1=generic internal no-argument classes. eg. clock widget. data1=argument_class_ref WARNING: given class should have pumpcall1 defined!
#2=(INTERNAL ONLY) gophermenu host+selector (NOT INTENDED FOR EXTERNAL URLS) data1=host, data2=selector
class xmitm:
	def __init__(self, icon, label, mtype, data1=None, data2=None, data3=None, comment="", width=350, height=100, resize=1):
		if isinstance(icon, pygame.Surface):
			self.icon=icon
		else:
			self.icon=pygame.image.load(os.path.join(libzox.gfxpath, icon))
		self.label=label
		self.mtype=mtype
		self.data1=data1
		self.data2=data2
		self.data3=data3
		self.comment=comment
		self.width=width
		self.height=height
		self.resize=resize
		#ensure if mtype==2 arguments sent to gopherpane are at least valid. if not set host+selector to splash page, print warning.
		if self.mtype==2:
			if self.data1==None:
				print("WARNING: xmitm entry: '" + label + "' of mtype 2, has no valid host given!\n    setting host+selector to internal default...")
				self.data1="zoxsplash>>"
				self.data2="/"
			if self.data2==None:
				print("WARNING: xmitm entry: '" + label + "' of mtype 2, has no valid selector given!\n    setting host+selector to internal default...")
				self.data1="zoxsplash>>"
				self.data2="/"
	def action(self):
		if self.mtype==2:
			newgop=gopherpane(host=self.data1, port=70, selector=self.data2)
			framesc.add_frame(stz.framex(self.width, self.height, self.label, resizable=self.resize, pumpcall=newgop.pumpcall1))
		if self.mtype==3:
			newgop=morethings(appselect=widgetslist, label="Widgets")
			framesc.add_frame(stz.framex(300, 400, self.label, resizable=True, pumpcall=newgop.pumpcall1))

		elif self.mtype==1:
			newgop=self.data1()
			framesc.add_frame(stz.framex(self.width, self.height, self.label, resizable=self.resize, pumpcall=newgop.pumpcall1))
	def render(self, frameobj, ypos):
		cache={}
		ystart=ypos
		#ensure background of card is white
		trectr=pygame.Rect(4, ypos, frameobj.sizex-9, frameobj.sizey)
		pygame.draw.rect(frameobj.surface, (232, 229, 217), trectr, 0)
		
		trectl=pygame.Rect(4, ypos, 71, frameobj.sizey)
		pygame.draw.rect(frameobj.surface, (86, 86, 86), trectl, 0)
		
		iconrect=frameobj.surface.blit(self.icon, (5, ypos+1))
		textrect1, ypos, cache = textitem(self.label, morefonthead, 24, (0, 0, 0), frameobj.surface, ypos, cache, xoff=77, textcoly=(232, 229, 217), roff=5)
		pygame.draw.line(frameobj.surface, (0, 0, 0), (5+self.icon.get_width(), ypos-1), (frameobj.sizex-7, ypos-1), 1)
		textrect2, ypos, cache = textitem(self.comment, morefontcomment, 20, (50, 50, 50), frameobj.surface, ypos, cache, xoff=77, textcoly=(232, 229, 217), roff=5)
		
		iconrect.w=frameobj.sizex-9
		iconrect.x-=1
		iconrect.y=ystart
		if ypos-ystart<72:
			iconrect.h=72
		else:
			iconrect.h=ypos-ystart
		
		pygame.draw.rect(frameobj.surface, (0, 0, 0), iconrect, 1)
		
		if ypos<72+ystart:
			ypos=72+ystart
		#
		endrect=pygame.Rect(4, ypos, frameobj.sizex-9, frameobj.sizey)
		pygame.draw.rect(frameobj.surface, (107, 107, 107), endrect, 0)
		shadowrect=pygame.Rect(0, ypos, frameobj.sizex-9-20, 20)
		pygame.draw.rect(frameobj.surface, (47, 47, 47), shadowrect, 0)
		
		#ypos+=1
		return (ypos, iconrect)
		

#Widgets Menu
widgetslist=[xmitm("more_clock.png", "Clock", 1, data1=libzoxui.clock, comment="An on-screen clock with date and sound.", width=230, height=60, resize=0),
xmitm("more_tipofday.png", "Tip Of The Day", 1, data1=libzoxui.tipofday, comment="Get a random tip from a set of Zoxenpher-related tips.", width=350, height=120, resize=0)]

#main category
defaultlist=[xmitm("more_dummy.png", "File Browse", 2, data1="file>>", data2="/", comment="Browse zoxenpher's subdirectories.", width=gopherwidth, height=gopherheight, resize=0),
xmitm("more_dummy.png", "Widgets ->", 3, data1=widgetslist, comment="A selection of assorted mini-programs of varying usefulness.",),
xmitm("more_sinfo.png", "System Info", 1, data1=libzoxui.sinfo, comment="Info on Zoxenpher's runtime, and host OS.", width=200, height=240, resize=0)]

testmenu=[xmitm("more_dummy.png", "TEST ITEM 02", 1, data1=gopherpane, comment="Hello", width=gopherwidth, height=gopherheight),
xmitm("more_dummy.png", "TEST ITEM 03", 1, data1=gopherpane, comment="Hello", width=gopherwidth, height=gopherheight),]

class morethings:
	def __init__(self, appselect=defaultlist, label="main"):
		self.yoff=25
		self.yjump=int(libzox.cnfdict["menutextjump"])
		self.data=0
		self.appselect=appselect
		self.scrollup=scrollup.convert()
		self.scrolldn=scrolldn.convert()
		self.scrollup_no=scrollup_no.convert()
		self.scrolldn_no=scrolldn_no.convert()
		self.label=label
	def renderdisp(self, frameobj):
		frameobj.surface.fill((107, 107, 107))
		self.ypos=self.yoff
		self.rectlist=[]
		for item in self.appselect:
			self.ypos, retrect = item.render(frameobj, self.ypos)
			self.rectlist.extend([[retrect, item]])
		self.ypos+=25
		self.hudrect=pygame.Rect(0, 0, frameobj.surface.get_width(), 22)
		pygame.draw.rect(frameobj.surface, (220, 220, 220), self.hudrect)
		if self.yoff<25:
			self.scuprect=frameobj.surface.blit(self.scrollup, (frameobj.surface.get_width()-24, 0))
		else:
			self.scuprect=frameobj.surface.blit(self.scrollup_no, (frameobj.surface.get_width()-24, 0))
		if self.ypos>frameobj.sizey:
			self.scdnrect=frameobj.surface.blit(self.scrolldn, (frameobj.surface.get_width()-46, 0))
		else:
			self.scdnrect=frameobj.surface.blit(self.scrolldn_no, (frameobj.surface.get_width()-46, 0))
		siderect=pygame.Rect(0, 0, 4, frameobj.sizey)
		#siderect2=pygame.Rect(frameobj.sizex-5, 0, 5, frameobj.sizey)
		pygame.draw.rect(frameobj.surface, (220, 220, 220), siderect)
		#pygame.draw.rect(frameobj.surface, (220, 220, 220), siderect2)
		pygame.draw.line(frameobj.surface, (0, 0, 0), (4, 0), (4, frameobj.sizey), 1)
		
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==2:
			self.renderdisp(frameobj)
		if frameobj.statflg==1:
			frameobj.seticon(more_wicon.convert())
			frameobj.name="More: "+self.label
			self.renderdisp(frameobj)
		if frameobj.statflg==4:
			mpos=stz.mousehelper(data.pos, frameobj)
			if not self.hudrect.collidepoint(mpos):
				if data.button==1:
					for item in self.rectlist:
						if item[0].collidepoint(mpos):
							item[1].action()
				elif data.button==4:
					self.yoff+=self.yjump*2
					if self.yoff>25:
						self.yoff=25
					self.renderdisp(frameobj)
				elif data.button==5 and self.ypos>frameobj.sizey:
					self.yoff-=self.yjump*2
					self.renderdisp(frameobj)
							
				

