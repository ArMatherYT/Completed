import pygame as pg
from pygame.math import Vector2 as V2
from random import randint as rnd

food, _ = lambda: V2(rnd(0,14),rnd(0,14)), pg.init()
DISP,KEY = pg.display.set_mode((600,600)),1073741903
pcs,fd,dr = [V2(7,7)], food(), V2(-1,0)
drs = {0:V2(1,0),1:V2(-1,0),2:V2(0,1),3:V2(0,-1)}

while pcs.count(pcs[0]) == 1:
    DISP.fill('black')
    for e in pg.event.get():
        if e.type == pg.QUIT: exit()
        if e.type == pg.KEYDOWN: dr=drs.get(e.key-KEY,dr)
    if pcs[0] == fd: fd, pcs = food(), pcs+[pcs[0]]
    for pc in pcs: pg.draw.rect(DISP,'green',(*40*pc,40,40))
    pg.draw.rect(DISP,'red',(*40*fd,40,40))
    [pcs.insert(0,pcs[0]+dr), pcs.pop(-1)]
    pcs[0].x, pcs[0].y = pcs[0].x%15, pcs[0].y%15
    pg.display.update(), pg.time.wait(100)