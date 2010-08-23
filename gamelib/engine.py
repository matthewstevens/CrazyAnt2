''' Engine that handles the interaction of the game logic and the underlying libraries
Like the cocos2d director it is a singleton.
'''

import cocos
from cocos.director import director
import cocos.layer as layer
import cocos.scene as scene
from cocos.sprite import Sprite

from data import resourceManager
from util_layers import HelloWorld, KeyDisplay, MouseDisplay, SplashScreenLayer, MenuBackground, MainMenu, OptionMenu
#from util_screens import MenuScreen, SplashScreen

class Level(object):
    """
    Test level to prototype how it all works
    """
    def __init__(self):
        self.layer = layer.Layer()
        self.character = Sprite(resourceManager.man)
        self.character.position = (100, 100)
        self.layer.add(self.character)
        self.scene = scene.Scene(self.layer)
    def get_scene(self):
        return self.scene

class Engine(object):
    def init(self):
        """
        Initialise the director, then load the levels
        Then create the scenes
        """
        director.init()
        self.scenes = {
            "SPLASH": self.create_splash(),
            "MENU": self.create_menus(),
        } 
        self.scenes.update(self.create_levels())

    def create_splash(self):
        return scene.Scene(SplashScreenLayer())
    def create_menus(self):
        layers = layer.MultiplexLayer(MainMenu(), OptionMenu())
        return scene.Scene(MenuBackground(), layers)
    def create_levels(self):
        config = resourceManager.config
        sections = config.sections()
        for section in sections:
            level_config = dict(config.items(section))
            print level_config
        self.level = Level()
        return {
            # FIXME - this needs replacing with levels
            #
            "GAME": self.level.get_scene()
        }
    def transition(self, name):
        director.replace(self.scenes[name])
    def push(self, name):
        director.push(self.scenes[name])
    def run(self): 
        hello_layer = HelloWorld()
        #main_scene = cocos.scene.Scene(hello_layer, KeyDisplay(), MouseDisplay())
        #cocos.director.director.run(main_scene)
        # start it off at the starting scene
        director.run(self.scenes["SPLASH"])

engine = Engine()
