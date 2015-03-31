import os
import subprocess
import threading

class cd:
    """Context manager for changing the current working directory"""
    lock = threading.RLock ()
    def __init__ ( self, newPath ):
        self.newPath = newPath

    def __enter__ ( self ):
        self.lock.acquire ()
        self.savedPath = os.getcwd ()
        os.chdir ( self.newPath )

    def __exit__ ( self, etype, value, traceback ):
        os.chdir ( self.savedPath )
        self.lock.release ()

def run_command ( command, ret = 'exit_code' ):
    r = None
    if ret == 'exit_code':
        r = subprocess.call ( command, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL )
    if ret == 'output':
        r = subprocess.check_output ( command, stderr = subprocess.DEVNULL )
        r = r.rstrip ( b'\n' )
    return r

def popen ( command, *args_forward, **keyargs ):
    return subprocess.Popen ( command, *args_forward, **keyargs )
