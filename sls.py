#!/usr/bin/env python

#
#                            Stochastic L-Systems
#
#
#                     Daniel Jones <dcjones@cs.washington.edu>
#                                 Nov. 5, 2010
#

'''
sls: stochastic  l-systems
'''

import cairo
from numpy        import array, sin, cos, pi
from numpy.random import uniform
from functools    import partial
from copy         import copy
from collections  import defaultdict
from sys          import stdout, stderr


tau = 2*pi # pi is wrong

def weighted_choice( ws ):
    if len(ws) == 0: raise IndexError
    if len(ws) == 1: return 0

    z = uniform( high = sum(ws) )
    for (i,w) in enumerate(ws):
        if z <= w: return i
        z -= w

    return len(ws)-1



#
# Section I. L-System Programs
#



class scfg:
    '''
    A representation of stochastic context free grammar.
    '''

    class op:
        def __init__( self, opcode = None, args = [] ):
            self.opcode = opcode
            self.args   = args

        def __repr__( self ):
            s = '%s' % self.opcode
            if self.args:
                s += '( '
                s += ', '.join( map(repr,self.args) )
                s += ' )'
            return s

    class rule:
        def __init__( self, nterm, ops, weight=1.0 ):
            self.nterm  = nterm
            self.ops    = ops
            self.weight = weight

        def __repr__( self ):
            s = '%s:%0.2f -> ' % (self.nterm,self.weight)
            s += ''.join(map(repr,self.ops))
            return s


    def __init__( self ):
        self.rules = defaultdict(list)


    def __call__( self, nterm ):
        if nterm not in self.rules: return None
        i = weighted_choice([ rule.weight for rule in self.rules[nterm] ])
        return self.rules[nterm][i]

    def __repr__( self ):
        s = str()
        for nterm in self.rules:
            for rule in self.rules[nterm]:
                s += '\t' + repr(rule) + '\n'
        return s

    def add_rule( self, rule ):
        self.rules[rule.nterm].append( rule )


    def render( self ):
        render( self )






#
# Section II. Predefined operators
#

def _check_params( n, m, f ):
    def g(s, args):
        if len(args) > m:
            raise Exception( "Too many arguments to %s" % f.__name__ )
        if len(args) < n:
            raise Exception( "Too few arguments to %s" % f.__name__ )
        return f( s, args )

    return g

def op( n, m=None ):
    return partial( _check_params, n, (m if m is not None and m >= n else n) )



@op(0,1)
def op_forward( s, args ):
    if args: delta = float(args[0])
    else:    delta = float(s.symb['F.delta'])

    s.line( delta )

@op(0,1)
def op_backward( s, args ):
    if args: delta = float(args[0])
    else:    delta = float(s.symb['B.delta'])

    s.line( -delta )

@op(0,1)
def op_left( s, args ):
    if args: delta = float(args[0])
    else:    delta = float(s.symb['+.delta'])

    s.turn( delta )

@op(0,1)
def op_right( s, args ):
    if args: delta = float(args[0])
    else:    delta = float(s.symb['-.delta'])

    s.turn( -delta )


@op(0)
def op_push( s, args ):
    stderr.write( '(push)' )
    sn = s.dup()
    sn.exp = None
    s.ss.append( sn )

@op(0)
def op_pop( s, args ):
    stderr.write( '(pop)' )
    sn = s.ss.pop()
    s.set(sn)
    s.restore()




#
# Section II. Rendering
#


def _default_symbol_table():
    return { 'F' : op_forward,
             'B' : op_backward,
             '+' : op_right,
             '-' : op_left,
             '[' : op_push,
             ']' : op_pop,
             'F.delta' : 50,
             'B.delta' : 50,
             '+.delta' : 0.1,
             '-.delta' : 0.1
             }



class state:

    def restore( self ):
        self.ctx.move_to( *self.xy )

    def set( self, s ):
        self.xy    = copy(s.xy)
        self.theta = s.theta
        self.k     = s.k


    def dup( self ):
        sn    = copy(self)
        sn.xy = copy(self.xy)
        return sn

    def move( self, delta ):
        self.xy += delta * array([cos(self.theta*tau), sin(self.theta*tau)])
        self.ctx.move_to( *self.xy )

    def line( self, delta ):
        self.xy += delta * array([cos(self.theta*tau), sin(self.theta*tau)])
        self.ctx.line_to( *self.xy )
        self.ctx.stroke()

    def turn( self, delta ):
        print (delta,self.theta)
        self.theta += delta

    def rel_line_to( self, delta ):
        pass


    def __init__( self, exp = [], k = 1, ctx = None, ss = None ):
        self.ss  = ss   # state stack
        self.ctx = ctx  # cairo context
        self.k   = k    # the recursion depth
        self.exp = exp  # the sequence of operations pending

        self.symb = _default_symbol_table()

        self.xy    = array( [0,0] ) # position
        self.theta = 0.125          # direction




def render_error( msg ):
    stderr.write( 'Error:' )
    stderr.write( msg )
    exit(1)




def render( surface, grammar, n, start_nterm = 'S' ):
    '''
    Render the given grammar on the given surface at a depth of n.
    '''

    # state stack
    ss = []

    # initial state
    s0 = state( exp = [scfg.op( 'S' )],
                ctx = cairo.Context(surface),
                ss  = ss )

    ss.append(s0)

    while ss:
        s = ss.pop()
        if s.k > n: continue

        print (s.k,s.exp)

        s.restore()


        for (i,op) in enumerate(s.exp):
            print '\t%r' % ((i,op.opcode),)

            # treat the opcode as a operator
            if op.opcode in s.symb:
                f = s.symb[op.opcode]
                f( s, op.args )


            # treat the opcode as a nonterminal
            rule = grammar(op.opcode)
            if rule:
                if i < len(s.exp)-1:
                    s.exp = s.exp[i+1:]
                    ss.append(s)

                if s.k + 1 <= n:
                    sn = s.dup()
                    sn.exp = rule.ops
                    sn.k   = s.k + 1
                    ss.append(sn)

                break

            if not (op.opcode in s.symb or rule):
                render_error( 'Unknown symbol %r\n' % op.opcode )



if __name__ == '__main__':
    pass

