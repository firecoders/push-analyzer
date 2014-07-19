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

import argparse
import os.path
import re

from utils import *

def parse_args ():
    parser = argparse.ArgumentParser ( description = 'Analyze changes to a git repository.' )
    parser.add_argument ( 'url', help = 'URL to the repository' )
    parser.add_argument ( '-i', '--interval', type = float, default = 20, help = 'The interval in which to poll' )
    parser.add_argument ( '-v', '--verbose', dest='verbosity', action = 'count', default = 0 )
    home_directory = os.path.expanduser ( '~' )
    parser.add_argument ( '-d', '--directory', default = home_directory + '/push-analyzer/', help = 'The directory to work in' )
    return parser.parse_args ()

def repo_folder ( url ):
    match = re.match( r".*/([^\.]*)", url )
    if not match:
        raise Exception ( "Not a valid git repository" )
    else:
        return match.group ( 1 )

args = parse_args ()
folder = repo_folder ( args.url )
