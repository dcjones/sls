

from collections import namedtuple

sls_ex = namedtuple( 'sls_ex', 'n code' )

examples = [
sls_ex( \
        n = 10,
        code = \
'''
# Foliage 1
S -> F(20)F(runif(20,50))X
X -> [-(rnorm(-0.01,0.03))FX]-(rnorm(0.01,0.02))FX
''' ),

sls_ex( \
        n = 12,
        code = \
'''
# Foliage 2
S -> +(0.02) F( 80/(1.4**k) ) [X] F [Y] S
X -> +(0.1) S
Y -> -(0.1) S
''' ),

sls_ex( \
        n = 12,
        code = \
'''
# Foliage 3
S -> +(0.02) F( 80/(1.4**k) ) [X] F [X] S
X -> +(0.1) S
X -> -(0.1) S
''' ),

sls_ex( \
        n = 2000,
        code = \
'''
# Drunkards Walk 1
S -> MX
X -> F(3) +(rnorm(0,0.08)) X
''' ),


sls_ex( \
        n = 60,
        code = \
'''
# Tiles 1
S -> MX
X -> F(20) +(0.25) X
X -> F(20) -(0.25) X
X:0.2 -> [X] +(0.25)X
X:0.2 -> [x] -(0.25)X
'''
),

sls_ex( \
        n = 60,
        code = \
'''
# Tiles 2
S -> MX
X -> F(20) +(1/3.0) X
X -> F(20) -(1/3.0) X
X:0.2 -> [X] +(1/3.0)X
X:0.2 -> [x] -(1/3.0)X
'''
),

sls_ex( \
        n = 6,
        code = \
'''
# Koch
S -> M(0,400) -(0.25) F
F -> F(3) +(0.25) F -(0.25) F - F + F
''' ),

sls_ex( \
        n = 10,
        code = \
'''
# Dragon Curve
S -> M F(10) X
X -> X +(0.25) Y F
Y -> F X -(0.25) Y
''' ),

sls_ex( \
        n = 4,
        code = \
'''
# Koch Island
S -> M(400,400) F(3) -(0.25) F - F - F
F -> F -(0.25) F +(0.25) F + F F - F - F + F
''' ),

sls_ex( \
        n = 5,
        code = \
'''
# Plant-Like A
S -> F(5)
F -> F [+F] F [-F] F
''' ),

sls_ex( \
        n = 6,
        code = \
'''
# Plant-Like B
S -> F(6)
F -> F [+F] F [-F] [F]
''' ),

sls_ex( \
        n = 5,
        code = \
'''
# Plant-Like C
S -> F(7)
F -> F F -(0.05) [-F+F+(0.05)F] + [+F-F-F]
''' ),

sls_ex( \
        n = 6,
        code = \
'''
# Plant-Like D
S -> F(3) [+(0.05)S] F [-(0.05)S] + S
F -> FF
''' ),

sls_ex( \
        n = 6,
        code = \
'''
# Plant-Like E
S -> F(3) [+(0.1)S] [-(0.1)S] F S
F -> FF
''' ),

sls_ex( \
        n = 5,
        code = \
'''
# Plant-Like F
S -> F(5) -(0.05) [[S] +(0.05) S] + F [+FS] - S
F -> FF
''' ),

sls_ex( \
        n = 5,
        code = \
'''
# Plant-Like E, with noise
S -> F(runif(2,8)) -(rnorm(0.05,0.01)) [[S] +(rnorm(0.05,0.01)) S] + F [+FS] - S
F -> FF
''' ),

sls_ex( \
        n = 5,
        code = \
'''
# Hexagonal Gosper Curve
F1 = F
F2 = F
S -> M F1(5)
F1 -> F1 +(1/6.0) F2(5) + + F2 - F1 -(1/6.0) - F1 F1 - F2 +
F2 -> -(1/6.0) F1 + F2 F2 + + F2 + F1 - - F1 - F2
''' ),

sls_ex( \
        n = 5,
        code = \
'''
# Koch D
S -> M(200,450) F(5) -(0.25) F - F - F
F -> F F -(0.25) F - - F - F
''' ),

sls_ex( \
        n = 5,
        code = \
'''
# Koch C
S -> M(200,300) F(5) -(0.25) F - F - F
F -> F F -(0.25) F +(0.25) F - F - F F
''' ),

sls_ex( \
        n = 6,
        code = \
'''
# Koch E
S -> M(300,50) F(5) -(0.25) F - F - F
F -> F -(0.25) F F -- F - F
''' )



]


