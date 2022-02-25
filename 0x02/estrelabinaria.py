GlowScript 3.1 VPython

scene.range = 5e11

# gravidade
G = 6.7e-11

# estrela grande vermelha 
bigstar = sphere(pos = vector(-2e11, 0, 0), radius = 2e10, color = color.red, make_trail = True, interval = 10)
bigstar.mass = 2e30
# quantidade de movimento estrela grande (Q=m*v)
bigstar.p = vector(0, 1e3, 0) * bigstar.mass

# estrela pequena amarela
smallstar = sphere(pos = vector(3e11, 0, 0), radius = 1e10, color = color.yellow, make_trail = True, interval = 10)
smallstar.mass = 1e30
# quantidade de movimento estrela pequena (Q=m*v)
smallstar.p = vector(0, -1e4, 0) * smallstar.mass 

sum.p = 0

dt = 1e5 # variaçao do tempo

# centro das massas
centerofmass = (bigstar.mass * bigstar.pos + smallstar.mass * smallstar.pos)/(bigstar.mass + smallstar.mass)

COM = cone(pos = centerofmass, axis = vector(0, 1e10, 0), radius = 1e10, color= color.green, make_trail = True)

scene.camera.follow(COM)

while True:
    rate(100)
    r = bigstar.pos - smallstar.pos
    # F: força gravitacional (F=G*M*m*r/rˆ2)
    F = G * bigstar.mass * smallstar.mass * r.hat / mag2(r) # hat: vetor unitario 
    
    bigstar.p = bigstar.p - F * dt
    smallstar.p = smallstar.p + F * dt
    sum.p = bigstar.p + smallstar.p
    
    # ec: energia cinetica (m*vˆ2/2)
    ec_bigstar = bigstar.mass * mag2(vector(0, 3e3, 0)) / 2
    ec_smallstar = smallstar.mass * mag2(vector(0, -1e4, 0)) / 2
    ec_sum = (bigstar.mass + smallstar.mass) * mag2(vector(0, 3e3, 0) + vector(0, -1e4, 0)) / 2
    
    # print(ec_bigstar) # result: 9e+36
    # print(ec_smallstar) # result: 5e+37
    # print(ec_sum) # result: 7.35e+37
    
    bigstar.pos = bigstar.pos + (bigstar.p/bigstar.mass) * dt
    smallstar.pos = smallstar.pos + (smallstar.p/smallstar.mass) * dt 
    COM.pos = (bigstar.mass * bigstar.pos + smallstar.mass * smallstar.pos)/(bigstar.mass + smallstar.mass)
    
    # print(bigstar.p,smallstar.p,sum.p) 
    