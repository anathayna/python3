GlowScript 3.1 VPython

chao=box(pos=vector(0,-.2,0),size=vector(10,.4,2), color=color.white)
bola=sphere(pos=vector(-5,1.1,0),radius=.1, color=color.yellow, make_trail=True)
r0=bola.pos
g=vector(0,-9.8,0)
bola.m=0.2
v0=10
theta=70*pi/180
bola.p=bola.m*v0*vector(cos(theta),sin(theta),0)

t=0
dt=0.001

while bola.pos.y>=0.1:
  rate(1000)
  Fnet=bola.m*g
  bola.p=bola.p+Fnet*dt
  bola.pos=bola.pos+bola.p*dt/bola.m
  t=t+dt

