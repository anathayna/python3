GlowScript 3.1 VPython

g = 9.8             
r = 0.2 
v0 = 10
theta0 = 80 

bola_de_basquete = sphere(pos=vector(0,0,0), radius=2*r, color=color.orange, make_trail=True)
bola_de_basquete.v = vector(v0*cos(radians(theta0)), v0*sin(radians(theta0)), 0)
bola_de_basquete.a = vector(0, -g, 0)

chao = box(pos = vector(5, 0, 0), width = 8, length = 20, height = 0.05, color = color.white)

t = 0
dt = 0.01

while t <= 5:
    rate(100)
    bola_de_basquete.v = bola_de_basquete.v + bola_de_basquete.a * dt
    bola_de_basquete.pos = bola_de_basquete.pos + bola_de_basquete.v * dt

    if bola_de_basquete.pos.y <= r:
        bola_de_basquete.v.y =  - 0.8*bola_de_basquete.v.y
        bola_de_basquete.pos.y = r

    t = t + dt
    print(t)


