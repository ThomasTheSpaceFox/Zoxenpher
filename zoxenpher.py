#!/usr/bin/env python
import os
import pygame

import libzoxphr.libgop as libgop
import libzoxphr.strazoloidwm as stz
import libzoxphr.libzoxapps as lza


#configuration (TODO: build options menu)

import libzoxphr.libzoxui as libzoxui
import libzoxphr.libzox as libzox
from libzoxphr.libzox import progobj
from libzoxphr.libzox import pathprogobj

print("Zoxenpher v3.0.0.indev")


#set some option variables inside strazoloidwm based upon cnf.dat settings.
stz.framestyle=int(libzox.cnfdict["framestyle"])
stz.wmfps=int(libzox.cnfdict["wmfps"])
resizable_desk=int(libzox.cnfdict["resizable"])
stz.hudsize=25
#calculate gopher menu window width and height. (needed by desktop class)
simplefont = pygame.font.SysFont(libzox.cnfdict["menufont"], int(libzox.cnfdict["menufontsize"]))
gopherwidth=((simplefont.size("_")[0])*81)+25+4
gopherheight=int(libzox.cnfdict["menuheight"])
stz.code12_askbeforequit=True

#desktop 'taskbar' icons
progs=[progobj(lza.gopherpane, pygame.image.load(os.path.join(libzox.gfxpath, "newwindow.png")), "goppane", "Gopher Menu", "GOPHER", gopherwidth, gopherheight, 1, key=pygame.K_n, mod=pygame.KMOD_CTRL, hint="Open a new gopher window. (CTRL+n)"),
progobj(lza.urlgo, pygame.image.load(os.path.join(libzox.gfxpath, "go.png")), "urlgo", "URL GO:", "urlgo", 500, 100, 1, key=pygame.K_g, mod=pygame.KMOD_CTRL, hint="Enter a Gopher URL to load. (CTRL+g)"),
progobj(lza.bookmarks, pygame.image.load(os.path.join(libzox.gfxpath, "bookmarks.png")), "bookmarks", "Bookmarks", "bookmarks", gopherwidth, gopherheight, 1, key=pygame.K_b, mod=pygame.KMOD_CTRL, hint="Open bookmarks. (CTRL+b)"),
progobj(lza.quitx, pygame.image.load(os.path.join(libzox.gfxpath, "exit.png")), "quit", "quit", "quit", gopherwidth, gopherheight, 1, key=pygame.K_q, mod=pygame.KMOD_CTRL, hint="quit. (CTRL+q)", side=1, ghost=1),
pathprogobj(lza.gopherpane, pygame.image.load(os.path.join(libzox.gfxpath, "help.png")), "goppane_HELP", "Gopher Menu", "GOPHER_HELP", gopherwidth, gopherheight, 1, host="zoxhelp>>", selector="/", key=pygame.K_F1, hint="Bring up a help menu. (F1)"),
progobj(lza.morethings, pygame.image.load(os.path.join(libzox.gfxpath, "more.png")), "more", "More", "MORE", 300, 400, 1, key=pygame.K_F2, hint="More things. (F2)"),
progobj(lza.mediaplay, pygame.image.load(os.path.join(libzox.gfxpath, "media.png")), "media", "Media", "MEDIA", gopherwidth, gopherheight, 1, key=pygame.K_F3, hint="Media Player (F3)")]

deskt=lza.deskclass(progs)
pygame.font.init()


#logical equivalent to the desktop's "frame"
deskframe=stz.desktop(int(libzox.cnfdict["deskw"]), int(libzox.cnfdict["deskh"]), "Zoxenpher v3.0.0.indev", pumpcall=deskt.pumpcall1, resizable=resizable_desk)

windowicon=pygame.image.load(os.path.join(libzox.gfxpath, "icon32.png"))

#init framescape window manager class
framesc=stz.framescape(deskframe, deskicon=windowicon, actbevel=(230, 230, 230), inactbevel=(200, 200, 200), framebg=(160, 160, 160), framefg=(255, 255, 255), actframebg=(60, 60, 110), actframefg=(255, 255, 255))


#init UI and APP libraries...
libzoxui.init(framesc, deskt)
lza.init(framesc, deskt)

#start wm process (takes over main thread)
framesc.process()
print("done.")
