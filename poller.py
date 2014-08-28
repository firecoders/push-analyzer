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

import utils

class Poller:
    def __init__ ( self, url, work_dir = utils.home_directory + '/push_analzyer/' , interval = 20 ):
        self.revisions = {}
        self.ref_change = utils.Signal ()
        self.repo_name = utils.extract_repo_name ( url )
        self.repo_dir = work_dir + self.repo_name
        self.interval = interval

    def handle_change ( self, refs_post ):
        stamp_pre = utils.last ( sorted ( self.revisions.keys () ) )
        stamp_post = utils.utc_timestamp ()
        self.revisions [ stamp_post ] = refs_post
        if stamp_pre != None:
            self.ref_change ( stamp_pre, stamp_post )

    def poll ( self ):
        ref_dict = utils.build_ref_dict ()
        if self.latest_refs () != ref_dict:
            self.handle_change ( ref_dict )
        utils.run_command ( [ 'git', 'remote', 'update' ] )
        utils.run_command ( [ 'git', 'remote', 'prune', 'origin' ] )

    def loop ( self ):
        while True:
            with utils.cd ( self.repo_dir ):
                self.poll ()
            time.sleep ( self.interval )

    def latest_refs ( self ):
        return utils.last ( [ self.revisions [ key ] for key in sorted ( self.revisions.keys () ) ] )
