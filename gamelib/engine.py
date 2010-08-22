''' Engine that handles the interaction of the game logic and the underlying libraries
Like the cocos2d director it is a singleton.
'''

import cocos
from cocos.director import director
import cocos.layer as layer
import cocos.scene as scene

from data import resourceManager
from util_layers import HelloWorld, KeyDisplay, MouseDisplay, SplashScreenLayer, MenuBackground, MainMenu, OptionMenu
#from util_screens import MenuScreen, SplashScreen

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
        return {}
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
