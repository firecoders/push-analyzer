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

import os
import subprocess
from datetime import datetime
import re

def utc_timestamp ():
    return datetime.utcnow ().timestamp ()

def last ( lst ):
    if len ( lst ) == 0:
        return None
    return lst [ -1 ]

def extract_repo_name ( url ):
    match = re.match( r".*/([^\.]*)", url )
    if not match:
        raise Exception ( "Not a valid git repository" )
    else:
        return match.group ( 1 )

home_directory = os.path.expanduser ( '~' )

# System interaction

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

# Git interaction

def build_ref_dict ():
    ref_dict = {}
    output = popen ( [ 'git', 'show-ref' ], stdout = subprocess.PIPE ).stdout
    regex = re.compile ( br"([A-Za-z0-9]{40}) refs/(?:heads/|remotes/)(\S*)" )
    for line in output:
        match = regex.match ( line )
        if not match:
            raise Exception ( 'failed to match regex on `git show-ref` output line' )
        ref_dict [ match.group ( 2 ) ] = match.group ( 1 )
    return ref_dict

def get_sha_range ( revision_range ):
    shas = []
    output = popen ( [ 'git', 'rev-list', '--pretty=oneline', '--reverse', revision_range ], stdout = subprocess.PIPE ).stdout
    regex = re.compile ( br"([A-Za-z0-9]{40})" )
    for line in output:
        match = regex.match ( line )
        if not match:
            raise Exception ( 'failed to match regex on `git rev-list --pretty=oneline` output line' )
        shas.append ( match.group ( 1 ) )
    return shas

def get_diff ( tree_ish, second = None ):
    command = [ 'git', 'diff-tree', '-p', '--no-commit-id', tree_ish ]
    if second:
        command.append ( second )
    return run_command ( command, ret = 'output' )

def is_ancestor ( commit, of ):
    return run_command ( [ 'git', 'merge-base', '--is-ancestor', of, commit ] ) == 0

def get_best_ancestor ( ref_list, commit ):
    current = None
    for ref in ref_list:
        res = run_command ( [ 'git', 'merge-base', ref, commit ], ret = 'output' )
        if not current or is_ancestor ( res, current ):
            current = res
    return current

# Observer pattern

class Signal:
    def __init__ ( self ):
        self.subscribers = []

    def subscribe ( self, subscriber ):
        self.subscribers.append ( subscriber )

    def unsubscribe ( self, subscriber ):
        self.subscribers.remove ( subscriber )

    def __call__ ( self, *args, **kwargs ):
        for subscriber in self.subscribers:
            subscriber ( *args, **kwargs )
