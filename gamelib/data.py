'''Simple data loader module.

Loads data files from the "data" directory shipped with a game.

Enhancing this to handle caching etc. is left as an exercise for the reader.
'''

from ConfigParser import ConfigParser
from cocos import tiles
import pyglet
import os

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

class ResourceManagerGroup:
    def __init__(self, path):
        self.__dict__.update(dict(
            #resource_mappings = {},
            cache = {},
            path = filepath(path)
        ))
    #def __setattr__(self, key, filename):
    #    self.resource_mappings[key] = os.path.join(self.path, filename)
    def __getattr__(self, key):
        if self.cache.has_key(key):
            resource = self.cache[key]
        else:
            path = os.path.join(self.path, key)
            resource = self.load_resource(path)
            self.cache[key] = resource
        return resource
    def load_resource(self, filename):
        return None

class LevelResourceManagerGroup(ResourceManagerGroup):
    def load_resource(self, filename):
        self.setup_dir(filename)
        self.setup_dir(os.path.dirname(filename))
        return tiles.Resource(
            os.path.join(
                filename,
                os.path.split(filename)[1] + ".xml"
            )
        )
    def setup_dir(self, dirname):
        if dirname not in pyglet.resource.path:
            pyglet.resource.path.append(dirname)
            pyglet.resource.reindex()


class ObjectResourceManagerGroup(ResourceManagerGroup):
    def load_resource(self, path):
        result = {}
        subdirs = os.listdir(path)
        for subdir in subdirs:
            sub_results = []
            subpath = os.path.join(path, subdir)
            files = os.listdir(subpath)
            files.sort()
            for file in files:
                sub_results.append(self.load_img(os.path.join(subpath, file)))
            result[subdir] = sub_results
        return result
    def load_img(self, file_name):
        return pyglet.image.load('hint.png', file=load(file_name))

class ResourceManager(object):
    def __init__(self):
        self.levels = LevelResourceManagerGroup('levels')
        self.objects = ObjectResourceManagerGroup('objects')

"""
class OldResourceManager(object):
    def __init__(self):
        self.__dict__.update(dict(
            resource_mappings = {},
            cache = {}
        ))
        # populate ourselves with the data from the data directory
        for filename in os.listdir(data_dir):
            key, _ = os.path.splitext(filename)
            self.__setattr__(key, filename)
    def __setattr__(self, key, filename):
        self.resource_mappings[key] = filename
    def __getattr__(self, key):
"""
"""
Precondition - setattr needs to have been called on this key
"""
"""
        try:
            resource = self.cache[key]
        except KeyError:
            resource = self.load_resource(self.resource_mappings[key])
            self.cache[key] = resource
        return resource
    def load_resource(self, filename):
        path = filepath(filename)
        if os.path.isdir(path):
            result = []
            files = os.listdir(path)
            files.sort()
            for file in files:
                print file
                result.append(self.load_resource(os.path.join(filename, file)))
            return result
        _ , extension = os.path.splitext(filename)
        if extension == '.cfg':
            config = ConfigParser()
            config.readfp(load(filename))
            return config
        elif extension == '.png':
            return image.load('hint.png', file=load(filename))
"""            
""" We can't find a mapping!!"""
"""
        raise Exception("We do not know how to load the resource: %s" % filename)
"""

resourceManager = ResourceManager()
