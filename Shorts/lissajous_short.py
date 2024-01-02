import numpy as np
import pygame as pg

_,DS,K,L,T=pg.init(),pg.display.set_mode((400,400)),1,1,5000
CLOCK=pg.time.Clock()
P = pg.surfarray.pixels3d(DS)

while True:
	DS.fill('black')
	[exit() for e in pg.event.get() if e.type==pg.QUIT]
	X=150*np.cos(np.linspace(0,int(K)*2*np.pi,T))+200
	Y=150*np.sin(np.linspace(0,L*2*np.pi,T))+200
	X,Y=X.astype(np.int64),Y.astype(np.int64)
	P[X,Y,:]=255
	pg.display.update()
	K += 5*CLOCK.tick(60)/1000
	if K >= 10: K,L=1,L+1