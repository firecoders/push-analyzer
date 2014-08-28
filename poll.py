# push_analzyer, A library for analyzing git pushes
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

from settings import args, folder
import utils

revisions = {}

ref_change = utils.Signal ()

def handle_change ( refs_post ):
    stamp_pre = last ( sorted ( revisions.keys () ) )
    stamp_post = utils.utc_timestamp ()
    revisions [ stamp_post ] = refs_post
    if stamp_pre != None:
        ref_change ( stamp_pre, stamp_post )

def poll ():
    ref_dict = utils.build_ref_dict ()
    if latest_refs () != ref_dict:
        handle_change ( ref_dict )
    utils.run_command ( [ 'git', 'remote', 'update' ] )
    utils.run_command ( [ 'git', 'remote', 'prune', 'origin' ] )

def loop ():
    while True:
        with utils.cd ( args.directory + folder ):
            poll ()
        time.sleep ( args.interval )

def latest_refs ():
    return last ( [ revisions [ key ] for key in sorted ( revisions.keys () ) ] )

def last ( lst ):
    if len ( lst ) == 0:
        return None
    return lst [ -1 ]
