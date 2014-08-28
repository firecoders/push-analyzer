# push_analyzer, A library for analyzing git pushes
# Copyright (c) 2014 firecoders
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import subprocess

class cd:
    """Context manager for changing the current working directory"""
    def __init__ ( self, newPath ):
        self.newPath = newPath

    def __enter__ ( self ):
        self.savedPath = os.getcwd ()
        os.chdir ( self.newPath )

    def __exit__ ( self, etype, value, traceback ):
        os.chdir ( self.savedPath )

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
