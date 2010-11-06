#!/usr/bin/env python

import sls
import re
from lepl import *


# To deal with the semantics of expressions, we need our own lexer.  In
# particular, SLSToken matches regular tokens, while SLSExpr matches an entire
# parenthesis enclosed expression.

@function_matcher
def SLSExpr( support, stream ):
    p = 0
    for (i,c) in enumerate(stream):
        if c == '(': p += 1
        elif c == ')':
            if p > 0: p -= 1
            else: return (stream[0:i],stream[i:])

    if p != 0: return None
    else:
        return (stream[0:i+1],stream[i+1:])


@function_matcher_factory()
def SLSToken( regexp ):
    regexp = r'\s*(' + regexp + ')\s*'
    def match( support, stream ):
        mat = re.match( regexp, str(stream) )
        if not mat: return None
        (i,j) = mat.span(1)
        (_,k) = mat.span(0)
        return (stream[i:j],stream[k:])
    return match




# Functions to build a scfg from the grammar.

def nop( x ): return x

def make_op( xs ):
    return [sls.scfg.op( xs[0], xs[1] if len(xs) > 1 else None )]

def make_rule( xs ):
    x0 = xs[0]
    ops = xs[1:]
    nterm = x0[0]

    if len(x0) > 1:
        return sls.scfg.rule( nterm=nterm, ops=ops, weight=float(x0[1]) )
    else:
        return sls.scfg.rule( nterm=nterm, ops=ops )



# The grammar itself.


equals    = SLSToken( r'=' )                       >> nop
colon     = SLSToken( r':' )                       >> nop
lparen    = SLSToken( r'\(' )                      >> nop
rparen    = SLSToken( r'\)' )                      >> nop
symb      = SLSToken( r'[a-zA-Z\+\-\[\]][0-9]*' )  >  nop
expr      = SLSExpr()                              >  nop
op        = symb & ~lparen & expr & ~rparen | symb >= make_op
ops       = Delayed()
ops      += op & ops | op                          >= nop
nterm     = symb | symb & ~colon & Float()         > nop
rule      = nterm & ~equals & ops                  >= make_rule



class ParserError:
    def __init__( self, k ):
        self.k = k


# Now that we can match rules, we simply parse each line
def parse( S ):
    if type(S) == str:
        S = S.split('\n')

    k = 1 # line number

    grammar = sls.scfg()
    for line in S:
        if re.match( r'^\s*$', line ): continue
        try:
            r = rule.parse(line)
        except:
            raise ParserError( k )

        grammar.add_rule( r )
        k += 1

    return grammar



