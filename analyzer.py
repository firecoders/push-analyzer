from utils import *
from settings import *

results = Signal ()

def analyze_ref_change ( sha_pre, sha_post, ref_name ):
    changes = []
    changes_overview = []

    removals = get_log ( sha_post + b'..' + sha_pre )
    removals.reverse ()

    additions = get_log ( sha_pre + b'..' + sha_post )
    additions.reverse ()

    moves = []
    for ( added_sha, _ ) in additions:
        added_diff = get_diff ( added_sha )
        for ( removed_sha, _ ) in removals:
            if added_diff == get_diff ( removed_sha ):
                moves.append ( { 'from' : removed_sha.decode (), 'to' : added_sha.decode () } )

    for ( sha, msg ) in removals:
        moved = False
        for m in moves:
            if m [ 'from' ] == sha.decode ():
                moved = True
        if not moved:
            changes.append ( { 'type' : 'remove', 'sha' : sha.decode (), 'msg' : msg.decode () } )

    for ( sha, msg ) in additions:
        move = None
        for m in moves:
            if m [ 'to' ] == sha.decode ():
                move = m
        if move:
            changes.append ( {
                'type' : 'move',
                'from' : move [ 'from' ], 'to' : move [ 'to' ],
                'msg' : msg.decode ()
            } )
        else:
            changes.append ( { 'type' : 'add', 'sha' : sha.decode (), 'msg' : msg.decode () } )

    if get_diff ( sha_pre, sha_post ).decode () == '':
        changes_overview.append ( 'same overall diff' )

    for change in changes:
        if changes_overview.count ( change [ 'type' ] ) == 0:
            changes_overview.append ( change [ 'type' ] )

    if len ( removals ) > 0:
        type_field = 'forced update'
    else:
        type_field = 'update'
    results ( {
        'type' : type_field, 'changes' : changes_overview,
        'name' : ref_name.decode (),
        'from' : sha_pre.decode (), 'to' : sha_post.decode ()
    } )

    for change in changes:
        results ( change )

def analyze_push ( refs_pre, refs_post ):
    for key in refs_pre.keys ():
        if key not in refs_post:
            results ( { 'type' : 'remove branch', 'name' : key.decode () } )
    for key in refs_post.keys ():
        if key not in refs_pre:
            results ( { 'type' : 'create branch', 'name' : key.decode () } )
            sha_post = refs_post [ key ]
            sha_pre = get_best_ancestor ( refs_pre.values (), sha_post )
            if sha_post != sha_pre:
                analyze_ref_change ( sha_pre, sha_post, key )
        else: # key in refs_pre
            sha_pre = refs_pre [ key ]
            sha_post = refs_post [ key ]
            if sha_pre != sha_post:
                analyze_ref_change ( sha_pre, sha_post, key )
