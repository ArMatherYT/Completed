import pygame as pg
DISP,_=pg.display.set_mode((480,480)),pg.init()
BD, P, CNT = ['','','','','','','','',''], 'X', 0
PS,FONT = {'X':'O','O':'X'},pg.font.SysFont('Arial',160)
while True:
    DISP.fill('black')
    if CNT==9: CNT,BD=0,['','','','','','','','','']
    for e in pg.event.get():
        if e.type==pg.QUIT: exit()
        if e.type==pg.KEYDOWN: BD=['','','','','','','','','']
        if e.type==pg.MOUSEBUTTONDOWN:
            i = int(e.pos[0]/160) + 3*int(e.pos[1]/160)
            if not BD[i]: BD[i],P,CNT=P,PS[P],CNT+1
    for i in range(9):
        rect=pg.Rect(160*(i%3),160*(i//3),160,160)
        pg.draw.rect(DISP,'white',rect,width=1)
        if not BD[i]: continue
        t = FONT.render(BD[i],True,'white')
        DISP.blit(t,t.get_rect(center=rect.center))
    pg.display.update()