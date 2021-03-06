#!/usr/bin/env python

import sls
import cairo
import cStringIO
import cgi
#import cgitb ; cgitb.enable()
import numpy.random
import time
import threading
from random       import choice
from sls.examples import examples
from sls.parser   import ParserError
from os.path      import basename
from urllib       import urlencode


width    = 800
height   = 500

prog = basename(__file__)





# Prevent rendering hugely complex images.
max_secs = 10
class RenderTimeout(Exception): pass



# If no code is specified, choose a random example
defaultcode = choice(examples)





def render_html(params):
    '''
    Write an html interface to sls.
    '''


    html_head = \
    '''
    <html>
    <head>
    <title>Stochastic L-Systems</title>
    <style media="screen" type="text/css">
    p    { text-align: center; font-family: Sans-serif; font-size: x-small }
    body { background-color: #000000; color: #ffffff }
    a:visited { color: #d0d0d0 }
    a:link    { color: #ffffff }
    textarea  { spellcheck: "false"; background-color: #101010; color: #ffffff; border: 0 }
    input     { spellcheck: "false"; background-color: #101010; color: #ffffff; border: 0 }
    </style>
    </head>
    <body>
    '''

    html_links = \
    '''
    <p>
    (<a href="slswww.py">random</a>)
    (<a href="instructions.html">instructions</a>)
    (<a href="https://github.com/dcjones/sls">source code</a>)
    '''
    html_links += '(<a href="%s?%s">author</a>)</p>\n' % (prog, urlencode( { 'code' : easter_egg_code }) )


    html_tail = \
    '''
    </body>
    </html>
    '''

    # make form submit and image url
    params['render'] = 1
    render_url = ('%s?' % prog) + urlencode(params)
    params['render'] = 0
    code = params['code']
    del params['code']
    submit_url = ('%s?' % prog) + urlencode(params)


    print 'Content-type: text/html\n'

    print html_head

    print '<p>(Stochastic L-Systems)</p>'
    print '<p><img width="%d" height="%d" src="%s"></p>' % (width,height,render_url)
    print '<form action="%s" method="post">' % (submit_url,)
    print '<p><textarea name="code" cols="60" rows="10">'
    print code
    print '</textarea></p>'
    print '<p>Depth: <input size="4" maxlength="4" type="text" name="n" value="%d" />' % params['n']
    print '<p><input type="submit" value="Render!" /></p>'
    print '</form>'
    print html_links

    print html_tail




def render_error( surface, error  ):
    '''
    When the L-system can not be rendered, render instead an error messege.
    '''

    ctx = cairo.Context( surface )

    ctx.set_source_rgb( 0, 0, 0 )
    ctx.paint()

    ctx.set_source_rgb( 1, 1, 1 )
    ctx.select_font_face( 'Courier' )
    ctx.set_font_size( 20 )

    msg = 'You fucked up!'
    (tw0,th0) = ctx.text_extents( msg )[2:4]
    ctx.move_to( width / 2.0 - tw0/2.0, height / 2.0 )
    ctx.show_text( msg )

    ctx.set_font_size( 14 )


    msg = '(' + type(error).__name__ + ') '
    (tw,th) = ctx.text_extents( msg )[2:4]
    ctx.move_to( width / 2.0 - tw/2.0, height / 2.0 + 2*th0 )
    ctx.show_text( msg )


    if type(error) == RenderTimeout:
        msg = 'Rendering your image is taking too long.'
    elif type(error) == ParserError:
        msg = 'Could not parse line %d of your program\n' % (error.k-1)
    else:
        msg = 'A mysterious, unidentifiable error occoured. Please report this.'

    (tw,th) = ctx.text_extents( msg )[2:4]
    ctx.move_to( width / 2.0 - tw/2.0, height / 2.0 + 3*th0 )
    ctx.show_text( msg )





def render_png(params):
    '''
    Write a PNG rendering of a l-system.
    '''

    class RenderThread(threading.Thread):
        def __init__( self, surface, w, h, grammar, n, max_pops=None ):
            threading.Thread.__init__( self )
            self.surface  = surface
            self.w        = w
            self.h        =h
            self.grammar  = grammar
            self.n        = n
            self.max_pops = max_pops

        def run( self ):
            sls.render( surface  = self.surface,
                        w        = self.w,
                        h        = self.h,
                        grammar  = self.grammar,
                        n        = self.n,
                        max_pops = self.max_pops )


    # render author image
    if params['code'].strip('\n\r') == easter_egg_code.strip('\n\r'):
        import bz2
        import binascii
        print "Content-type: image/jpeg\n"
        print bz2.decompress(binascii.a2b_base64(easter_egg_img.replace('\n','')))
        return


    surface = cairo.ImageSurface( cairo.FORMAT_ARGB32, width, height )

    try:
        grammar = sls.parse(params['code'])

        t = RenderThread( surface  = surface,
                          w        = width,
                          h        = height,
                          grammar  = grammar,
                          n        = params['n'],
                          max_pops = None )

        t.start()
        t.join( max_secs )

        if t.isAlive():
            raise RenderTimeout

    except Exception as error:
        surface = cairo.ImageSurface( cairo.FORMAT_ARGB32, width, height )
        render_error( surface, error )


    img = cStringIO.StringIO()
    surface.write_to_png( img )

    img.seek(0)
    print "Content-type: image/png\n"
    print img.read()




def main():
    form = cgi.FieldStorage()

    def param( key, default, valtype=str ):
        return (key, valtype(form.getfirst(key)) if key in form \
                     else valtype(default))

    params = dict( [
                param( 'seed', int(time.time()), int ),
                param( 'render', 0, int ),
                param( 'n', defaultcode.n, int ),
                param( 'code', defaultcode.code, str ) ] )

    numpy.random.seed( params['seed'] )
    params['seed'] = int(time.time())
    params['code'] = params['code'].strip('\n')

    if params['render']:
        render_png(params)
    else:
        render_html(params)







easter_egg_code = \
'''
Daniel Jones
Computer Science and Engineering
University of Washington

Send comments and suggestions to,
<dcjones@cs.washington.edu>
'''

easter_egg_img = \
'''
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
'''




if __name__ == '__main__':
    main()


