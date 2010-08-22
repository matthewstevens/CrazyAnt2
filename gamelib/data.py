'''Simple data loader module.

Loads data files from the "data" directory shipped with a game.

Enhancing this to handle caching etc. is left as an exercise for the reader.
'''

from ConfigParser import ConfigParser
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
        self.__dict__.update(dict(
            resource_mappings = {},
            cache = weakref.WeakValueDictionary()
        ))
        # populate ourselves with the data from teh data directory
        for filename in os.listdir(data_dir):
            key, _ = os.path.splitext(filename)
            self.__setattr__(key, filename)
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
            resource = self.load_resource(self.resource_mappings[key])
            self.cache[key] = resource
        return resource
    def load_resource(self, filename):
        _ , extension = os.path.splitext(filename)
        if extension == '.cfg':
            config = ConfigParser()
            config.readfp(load(filename))
            return config
        else:
            """ We can't find a mapping!!"""
            return None

resourceManager = ResourceManager()
