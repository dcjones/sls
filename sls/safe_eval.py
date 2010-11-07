import threading

'''
safe_eval
---------
Prevent eval code from running out of control by instating a time limit.
'''


class SafeEvalTimeout(Exception): pass



class SafeEvalThread(threading.Thread):
    def __init__( self, code, context ):
        threading.Thread.__init__( self )
        self.code    = code
        self.context = context
        self.result  = None

    def run( self ):
        if self.context:
            self.result = eval( self.code, self.context )
        else:
            self.result = eval( self.code )



def safe_compile( code ):
    return compile( code, '<sls-expr>', 'eval' )



def safe_eval( code, context = None, max_secs = None ):
    t = SafeEvalThread( code, context )
    t.start()
    t.join(max_secs)

    if t.isAlive():
        raise SafeEvalTimeout

    return t.result



