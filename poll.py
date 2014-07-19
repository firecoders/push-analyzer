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
