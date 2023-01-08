import pygame as pg, numpy as np

DISP,_ = pg.display.set_mode((500,500)), pg.init()
BD, RNG = np.zeros((10,10)), [-1, 0, 1]
BD[5,5]=BD[6,5]=BD[7,5]=BD[7,4]=BD[6,3]=1
F = lambda x,y:sum([
    BD[(x+w)%10,(y+h)%10] for h in RNG for w in RNG
])-BD[x,y]

while True:
    nbd, _ = np.zeros((10,10)), DISP.fill('black')
    [exit() for e in pg.event.get() if e.type==pg.QUIT]
    for y in range(10):
        for x in range(10):
            rect,a,b = (x*50,y*50,50,50), F(x,y), BD[x,y]
            if BD[x,y]: pg.draw.rect(DISP, 'pink', rect)
            pg.draw.rect(DISP, 'white', rect, width=1)
            if a==3 and b==0: nbd[x,y]=1
            elif (a<2 or a>3) and b==1: nbd[x,y]=0
            else: nbd[x,y]=b
    BD,*_=nbd.copy(),pg.display.update(),pg.time.wait(100)