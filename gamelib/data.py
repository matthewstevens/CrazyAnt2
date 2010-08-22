'''Simple data loader module.

Loads data files from the "data" directory shipped with a game.

Enhancing this to handle caching etc. is left as an exercise for the reader.
'''

import os
import weakref

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))

def filepath(filename):
    '''Determine the path to a file in the data directory.
    '''
    return os.path.join(data_dir, filename)

def load(filename, mode='rb'):
    '''Open a file in the data directory.

    "mode" is passed as the second arg to open().
    '''
    return open(os.path.join(data_dir, filename), mode)

class ResourceManager(object):
    def __init__(self):
        self.resource_mappings = {}
        self.cache = weakref.WeakValueDictionary()
    def __setattr__(self, key, filename):
        self.resource_mappings[key] = filename
    def __getattr__(self, key):
        """
        Precondition - setattr needs to have been called on this key
        """
        try:
            resource = self.cache[key]
        except KeyError:
            resource = None # FIXME - load something
            self.cache[key] = resource
        return resource
