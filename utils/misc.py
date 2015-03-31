import os
from datetime import datetime
import re

def utc_timestamp ():
    return datetime.utcnow ().timestamp ()

def last ( lst ):
    if len ( lst ) == 0:
        return None
    return lst [ -1 ]

home_directory = os.path.expanduser ( '~' )
