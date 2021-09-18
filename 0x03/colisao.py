GlowScript 3.1 VPython

scene = canvas(background = color=vec(0.667, 0.667, 0.667))

mesa=box(pos=vector(0,-.05,0), color=vec(0.239, 0.600, 0.439), size=vector(1,.1,.1))

bola=sphere(pos=vector(-.5,.5,0), radius=.05, texture="https://i.imgur.com/NKhSCH0.jpg", make_trail=True)
bola.m=.1
bola.v=vector(.5,-.5,0)
bola.p=bola.m*bola.v

t=0
dt=0.001
k=200

while bola.pos.x<.5:
    rate(1000)
    F=vector(0,0,0)
    if bola.pos.y<bola.radius:
        F=norm(vector(0,1,0))*(bola.radius-bola.pos.y)*k
    bola.p=bola.p+F*dt
    bola.pos=bola.pos+bola.p*dt/bola.m
    t=t+dt

