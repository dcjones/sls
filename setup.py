#!/usr/bin/env python

from setuptools import setup

setup( name         = 'sls',
       version      = '0.1',
       author       = 'Daniel Jones',
       author_email = 'dcjones@cs.washington.edu',
       description  = 'Stochastic L-Systems',
       url          = 'http://www.kopophex.com/sls',
       requires     = [ 'lepl',
                        'cairo',
                        'numpy',
                        'argparse',
                        'python (>=2.6, <3.0)' ],
       py_modules   = [ 'sls.core', 'sls.parser', 'sls.safe_eval', 'sls.examples' ],
       scripts      = [ 'scripts/sls' ]
       )


