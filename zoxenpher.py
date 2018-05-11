#!/usr/bin/env python
import time
import os
import libgop
import pygame
from threading import Thread
import strazoloidwm as stz
import copy
print("Zoxenpher v2.0.1")
#configuration (TODO: build options menu and config file)
#number of images loaded for preview. (images not previewed will be shown as links)
maximages=10

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


simplefont = pygame.font.SysFont("mono", 15)
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
			if self.hoverprev!=self.hovertext:
				self.hoverprev=self.hovertext
				self.drawdesk(frameobj.surface)
		#init code
		if frameobj.statflg==1:
			self.drawdesk(frameobj.surface)
		#shutdown code
		if frameobj.statflg==3:
			print("shutting down...")
			self.active=0
		#click event processing
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
			
		urllabel=simplefont.render(self.hovertext, True, (255, 255, 255), (60, 60, 120))
		surface.blit(urllabel, (icnx+10, 10))
		surface.blit(self.mascot, (surface.get_width()-self.mascot.get_width(), 0))
		


class progobj:
	def __init__(self, classref, icon, idcode, friendly_name, commname, xsize, ysize, resizable=0, key=None, mod=None):
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


class pathprogobj:
	def __init__(self, classref, icon, idcode, friendly_name, commname, xsize, ysize, resizable=0, key=None, mod=None, host="about:splash", port=70, selector="/"):
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
	def classref(self):
		return self.classrefx(host=self.host, port=self.port, selector=self.selector)

#run in a thread for each time a page is rendered the first time.
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


def textshow(host, port, selector):
	data=pathfigure(host, port, selector, gtype="0")
	menu=libgop.menudecode(data, txtflg=1)
	newgop=gopherpane(host=host, port=port, selector=selector, preload=menu, prefix="text: gopher://", gtype="0", shortprefix="text: ")
	framesc.add_frame(stz.framex(600, 500, "Text Document", resizable=1, pumpcall=newgop.pumpcall1, xpos=20))



		
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
					else:
						item.rect, self.ypos, self.renderdict = textitem("[IMAGE]" + item.name, simplefont, self.yjump, (0, 0, 255), frameobj.surface, self.ypos, self.renderdict)
					#pygame.draw.rect(frameobj.surface, (255, 255, 0), item.rect, 1)
				except AttributeError:
					item.image=None
					if imagecount<maximages or (imagecount<2 and self.forceimage):
						imageset.extend([item])
					
						
				
					
			else:
				rects, self.ypos, self.renderdict = textitem("[UNKNOWN:" + item.gtype + "]" + item.name, simplefont, 15, (0, 0, 0), frameobj.surface, self.ypos, self.renderdict)
				#print(item.gtype)
		#launch image loader thread if needed
		if imageset!=[]:
			sideproc=Thread(target = imgget, args = [imageset, self.menudraw, frameobj])
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
			deskt.hovertext=""
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
		if frameobj.statflg==4:
			if data.button==1 and not self.linkdisable:
				for item in self.menu:
					if item.gtype=="1":
						if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
							self.menu=[]
							sideproc=Thread(target = self.menuchange, args = [item, frameobj])
							sideproc.start()
							break
					if item.gtype=="0":
						if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
							sideproc=Thread(target = textshow, args = [item.hostname, item.port, item.selector])
							sideproc.start()
							break
					if item.gtype=="g" or item.gtype=="p" or item.gtype=="I":
						if item.rect.collidepoint(stz.mousehelper(data.pos, frameobj)):
							itemcopy=copy.deepcopy(item)
							del itemcopy.image
							newgop=gopherpane(host=itemcopy.hostname, port=itemcopy.port, selector=itemcopy.selector, prefix="image: gopher://", preload=[itemcopy], forceimage=1, linkdisable=1, gtype=item.gtype, shortprefix="image: ")
							framesc.add_frame(stz.framex(600, 500, "Image", resizable=1, pumpcall=newgop.pumpcall1, xpos=50, ypos=50))
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
			


class querypane:
	def __init__(self, host, port, selector):
		self.host=host
		self.port=port
		self.selector=selector
		self.yoff=0
		
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
		try:
			data=libgop.gopherget(self.host, self.port, self.selector, query=self.stringblob)
		except Exception:
			data=open(os.path.join("vgop", "gaierror"))
		menu=libgop.menudecode(data)
		newgop=gopherpane(host=self.host, port=self.port, selector=self.selector, preload=menu)
		framesc.add_frame(stz.framex(600, 500, "Gopher Menu", resizable=1, pumpcall=newgop.pumpcall1))
		#close self
		framesc.close_pid(frameobj.pid)
	def pumpcall1(self, frameobj, data=None):
		
		if frameobj.statflg==2:
			self.renderdisp(frameobj)
		if frameobj.statflg==1:
			str1=self.host+"/7"+self.selector
			print("querypane:")
			print(str1)
			frameobj.name="query: "+str1
			self.renderdisp(frameobj)
		if frameobj.statflg==6:
			if data.key==pygame.K_RETURN:
				if self.debug==1:
					print(self.stringblob)
				else:
					sideproc=Thread(target = self.loader, args = [frameobj])
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
				
		










class urlgo:
	def __init__(self):
		self.yoff=0
		self.yjump=15
		self.stringblob=""
		self.validchars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890:/.-_"
	def renderdisp(self, frameobj):
		frameobj.surface.fill((255, 255, 255))
		textitem("Please Type URL", simplefont, self.yjump, (0, 0, 0), frameobj.surface, self.yjump*2, {})
		textitem("gopher://"+self.stringblob+"|", simplefont, self.yjump, (14, 0, 14), frameobj.surface, self.yjump*4, {})
	def loaderg1(self, frameobj):
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
		if frameobj.statflg==2:
			self.renderdisp(frameobj)
		if frameobj.statflg==1:
			
			print("URLGO:")
			frameobj.name="URL GO:"
			self.renderdisp(frameobj)
		if frameobj.statflg==6:
			if data.key==pygame.K_RETURN:
				try:
					
					if self.stringblob.startswith("about:"):
						self.host=self.stringblob
						self.port=70
						self.selector=""
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
						sideproc.start()
					elif self.gtype=="0":
						sideproc=Thread(target = self.loaderg0, args = [frameobj])
						sideproc.start()
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
				





#desktop icons
progs=[progobj(gopherpane, pygame.image.load(os.path.join("vgop", "newwindow.png")), "goppane", "Gopher Menu", "GOPHER", 600, 500, 1, key=pygame.K_n, mod=pygame.KMOD_CTRL),
progobj(urlgo, pygame.image.load(os.path.join("vgop", "go.png")), "urlgo", "URL GO:", "urlgo", 400, 100, 0, key=pygame.K_g, mod=pygame.KMOD_CTRL),
pathprogobj(gopherpane, pygame.image.load(os.path.join("vgop", "help.png")), "goppane_HELP", "Gopher Menu", "GOPHER_HELP", 600, 500, 1, host="about:help", key=pygame.K_F1)]
deskt=deskclass(progs)
pygame.font.init()



desk=stz.desktop(800, 600, "Zoxenpher", pumpcall=deskt.pumpcall1, resizable=1)

windowicon=pygame.image.load(os.path.join("vgop", "icon32.png"))
framesc=stz.framescape(desk, deskicon=windowicon)

sideproc=Thread(target = deskt.process, args = [])
sideproc.start()







#start wm
framesc.process()




