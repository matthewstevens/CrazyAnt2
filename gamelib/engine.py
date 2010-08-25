''' Engine that handles the interaction of the game logic and the underlying libraries
Like the cocos2d director it is a singleton.
'''

import cocos
from cocos.director import director
from cocos import layer
from cocos import scene
from cocos import tiles
from cocos.sprite import Sprite
from cocos.actions import Action
from pyglet import image

from data import resourceManager
from util_layers import HelloWorld, KeyDisplay, MouseDisplay, SplashScreenLayer, MenuBackground, MainMenu, OptionMenu
#from util_screens import MenuScreen, SplashScreen

class Level(scene.Scene):

    is_event_handler = True

    """
    Test level to prototype how it all works
    """
    def __init__(self):
        super(Level, self).__init__()

        self.manager = layer.ScrollingManager(director.window)

        self.map = resourceManager.levels.level1['level1']
        self.manager.add(self.map)
        self.add(self.map, z=1)

        frames = resourceManager.objects.character['manstanding']
        print len(frames)
        animation = image.Animation.from_image_sequence(frames, 0.4)
        self.character = Sprite(animation, position = (100, 100))
        self.char_layer = layer.ScrollableLayer()
        self.char_layer.add(self.character)
        self.add(self.char_layer, z=2)
        self.manager.add(self.char_layer)
        #self.layer = layer.Layer()
        #self.character = Sprite(resourceManager.mananim)
        #self.layer.add(self.character)
        #self.manager.add(self.character)
        #self.scene = scene.Scene(self.layer)
        #self.scene = scene.Scene(self)
        #
        #self.scene.do(LevelAction())
        #self.do(LevelAction())
        self.manager.set_focus(-100, -100)
    def step(self, dt):
        #print 'ping'
        pass
    def get_scene(self):
        return self.scene
    def on_key_press(self, symbol, modifiers):
        print 'ouch'
    def on_key_release(self, symbo, modifiers):
        print 'aaah'

class LevelAction(Action):
    def step(self, dt):
        #x, y, = self.target.char_layer.position
        #self.target.manager.set_focus(int(x), int(y))
        #print 'ping'
        pass

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
        """
        FIXME - do we need a config, seems pointless
        config = resourceManager.config
        sections = config.sections()
        for section in sections:
            level_config = dict(config.items(section))
            print level_config
        """
        self.level = Level()
        return {
            # FIXME - this needs replacing with levels
            #
            "GAME": self.level
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
