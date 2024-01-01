import pygame as pg

DISP,U,D=pg.display.set_mode((500,500)),pg.K_UP,pg.K_DOWN
L,R,B,BD=250,250,pg.Vector2(250,250), pg.Vector2(-5,-5)

while True:
    K,_ = pg.key.get_pressed(), DISP.fill('black')
    [exit() for e in pg.event.get() if e.type==pg.QUIT]
    L += -5*int(K[119] and L>=100)+5*int(K[115] and L<=400)
    R += -5*int(K[U] and R>=100)+5*int(K[D] and R<=400)
    pg.draw.rect(DISP,'white',(20,L-100,20,200))
    pg.draw.rect(DISP,'white',(460,R-100,20,200))
    pg.draw.circle(DISP,'white',B,10)
    BD.x-=(2*BD.x*((B.x==40)*(abs(L-B.y)<100)+
    (B.x==460)*(abs(R-B.y)<100)))
    if B.y in (10, 490): BD.y *= -1
    if B.x < 10 or B.x > 490: B.x,B.y,BD=250,250,-BD 
    pg.display.update(), pg.time.wait(16), (B:=B+BD)