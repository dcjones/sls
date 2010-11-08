

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
''' )

]


