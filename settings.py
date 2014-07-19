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
        error ( "Not a valid git repository" )
    else:
        return match.group ( 1 )

args = parse_args ()
folder = repo_folder ( args.url )
