#!/bin/python

import pathlib
import threading

from utils import *
from settings import *
import poll
import analyzer

def analyze ( stamp_pre, stamp_post ):
    refs_pre = poll.revisions [ stamp_pre ]
    refs_post = poll.revisions [ stamp_post ]
    analyzer.analyze_push ( refs_pre, refs_post )

def print_formatted ( result ):
    print ( result )

poll.ref_change.subscribe ( analyze )
analyzer.results.subscribe ( print_formatted )

if __name__ == "__main__":
    run_command ( [ 'mkdir', '-p', args.directory ] )
    if not pathlib.Path ( args.directory + folder ).exists ():
        with cd ( args.directory ):
            run_command ( [ 'git', 'clone', args.url ] )
    threading.Thread ( target = poll.loop ).start ()
