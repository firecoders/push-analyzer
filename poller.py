import time
import pathlib

from . import utils
from .utils import misc
from .utils import system
from .utils import git
from .utils import observer

class Poller:
    def __init__ ( self, url, work_dir = utils.misc.home_directory + '/push_analzyer/' , interval = 20 ):
        self.revisions = {}
        self.ref_change = utils.observer.Signal ()
        self.repo_name = utils.git.extract_repo_name ( url )

        self.repo_dir = work_dir + self.repo_name
        self.interval = interval
        self.work_dir = work_dir
        self.url = url
        self.active = True

    def handle_change ( self, refs_post ):
        stamp_pre = utils.misc.last ( sorted ( self.revisions.keys () ) )
        stamp_post = utils.misc.utc_timestamp ()
        self.revisions [ stamp_post ] = refs_post
        if stamp_pre != None:
            self.ref_change ( stamp_pre, stamp_post )

    def poll ( self ):
        ref_dict = utils.git.build_ref_dict ()
        if self.latest_refs () != ref_dict:
            self.handle_change ( ref_dict )
        utils.system.run_command ( [ 'git', 'remote', 'update' ] )
        utils.system.run_command ( [ 'git', 'remote', 'prune', 'origin' ] )

    def stop ( self ):
        self.active = False

    def loop ( self ):
        utils.system.run_command ( [ 'mkdir', '-p', self.work_dir ] )
        if not pathlib.Path ( self.repo_dir ).exists ():
            with utils.system.cd ( self.work_dir ):
                utils.system.run_command ( [ 'git', 'clone', self.url ] )
        while self.active:
            with utils.system.cd ( self.repo_dir ):
                self.poll ()
            time.sleep ( self.interval )

    def latest_refs ( self ):
        return utils.misc.last ( [ self.revisions [ key ] for key in sorted ( self.revisions.keys () ) ] )
