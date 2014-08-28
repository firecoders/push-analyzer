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

from . import utils
from .utils import git

def analyze_ref_change ( sha_pre, sha_post, ref_name ):
    removals = utils.git.get_sha_range ( sha_post + b'..' + sha_pre )
    additions = utils.git.get_sha_range ( sha_pre + b'..' + sha_post )

    moves = []
    for added_sha in additions:
        added_diff = utils.git.get_diff ( added_sha )
        for removed_sha in removals:
            if added_diff == utils.git.get_diff ( removed_sha ):
                moves.append ( { 'from' : removed_sha.decode (), 'to' : added_sha.decode () } )

    changes = []

    for sha in removals:
        moved = any ( move [ 'from' ] == sha.decode () for move in moves )
        if not moved:
            changes.append ( { 'type' : 'remove', 'sha' : sha.decode () } )

    for sha in additions:
        move = next ( ( m for m in moves if m [ 'to' ] == sha.decode () ), None )
        if move:
            changes.append ( { 'type' : 'move', 'from' : move [ 'from' ], 'to' : move [ 'to' ] } )
        else:
            changes.append ( { 'type' : 'add', 'sha' : sha.decode () } )

    changes_overview = []

    for change in changes:
        if change [ 'type' ] not in changes_overview:
            changes_overview.append ( change [ 'type' ] )

    if utils.git.get_diff ( sha_pre, sha_post ).decode () == '':
        changes_overview.append ( 'same overall diff' )

    if len ( removals ) > 0:
        type_field = 'forced update'
    else:
        type_field = 'update'

    results = []

    results.append ( {
        'type' : type_field, 'changes' : changes_overview,
        'name' : ref_name.decode (),
        'from' : sha_pre.decode (), 'to' : sha_post.decode ()
    } )

    for change in changes:
        results.append ( change )

    return results

def analyze_push ( refs_pre, refs_post ):
    results = []

    for key in refs_pre.keys ():
        if key not in refs_post:
            results.append ( { 'type' : 'remove branch', 'name' : key.decode () } )
    for key in refs_post.keys ():
        if key not in refs_pre:
            results.append ( { 'type' : 'create branch', 'name' : key.decode () } )
            sha_post = refs_post [ key ]
            sha_pre = utils.git.get_best_ancestor ( refs_pre.values (), sha_post )
            if sha_post != sha_pre:
                results.extend ( analyze_ref_change ( sha_pre, sha_post, key ) )
        else: # key in refs_pre
            sha_pre = refs_pre [ key ]
            sha_post = refs_post [ key ]
            if sha_pre != sha_post:
                results.extend ( analyze_ref_change ( sha_pre, sha_post, key ) )

    return results
