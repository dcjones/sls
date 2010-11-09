

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
        n = 1000,
        code = \
'''
# Drunkards Walk 1
S -> MX
X -> F(10) +(rnorm(0,0.1)) X
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
)

]


