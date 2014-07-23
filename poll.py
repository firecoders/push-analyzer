# push-analyzer, A script for analyzing git pushes
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

import time

from settings import *
from utils import *

revisions = {}

ref_change = Signal ()

def handle_change ( refs_post ):
    stamp_pre = last ( sorted ( revisions.keys () ) )
    stamp_post = utc_timestamp ()
    revisions [ stamp_post ] = refs_post
    if stamp_pre != None:
        ref_change ( stamp_pre, stamp_post )

def poll ():
    run_command ( [ 'git', 'remote', 'update' ] )
    run_command ( [ 'git', 'remote', 'prune', 'origin' ] )
    ref_dict = build_ref_dict ()
    if last ( list ( [ revisions [ key ] for key in sorted ( revisions.keys () ) ] ) ) != ref_dict:
        handle_change ( ref_dict )

def loop ():
    while True:
        with cd ( args.directory + folder ):
            poll ()
        time.sleep ( args.interval )

def last ( lst ):
    if len ( lst ) == 0:
        return None
    return lst [ len ( lst ) - 1 ]
