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

class CharacterLayer(layer.ScrollableLayer):
    is_event_handler = True
    def __init__(self, manager):
        self.manager = manager
        super(CharacterLayer, self).__init__()
        frames = resourceManager.objects.character['manstanding']
        animation = image.Animation.from_image_sequence(frames, 0.4)
        self.character = Sprite(animation, (100, 306))
        #self.position = 
        self.add(self.character)
        self.do(LevelAction())
        self.move_vec = 0
    def on_key_press(self, symbol, modifiers):
        print 'ouch'
        if symbol == ord('a'):
            self.move_vec -= 1
        elif symbol == ord('d'):
            self.move_vec += 1
    def on_key_release(self, symbol, modifiers):
        print 'aaah'
        if symbol == ord('a'):
            self.move_vec += 1
        elif symbol == ord('d'):
            self.move_vec -= 1


class Level(scene.Scene):


    """
    Test level to prototype how it all works
    """
    def __init__(self):
        super(Level, self).__init__()

        self.manager = layer.ScrollingManager(director.window)

        self.map = resourceManager.levels.level1['level1']
        self.map.set_view(0, 0, 640, 480)

        self.manager.add(self.map, z = 1)
        self.manager.set_focus(100, 100)

        self.char_layer = CharacterLayer(self.manager)
        self.manager.add(self.char_layer, z = 2)
        self.add(self.manager)
        #self.do(LevelAction())
        #self.manager.set_focus(-100, -100)
    def step(self, dt):
        #print 'ping'
        pass
    def get_scene(self):
        return self.scene

class LevelAction(Action):
    def step(self, dt):
        x, y, = self.target.character.position
        vec = self.target.move_vec
        if vec:
            print "foo"
            print dt
            x += dt * vec *20 
            self.target.character.position = x, y
            #self.target.set_focus(x, y)
            self.target.manager.set_focus(int(x), int(y))

class Engine(object):
    def init(self):
        """
        Initialise the director, then load the levels
        Then create the scenes
        """
        director.init()
        director.window.set_caption("Captured Under Thread")
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
        """
        map = resourceManager.levels.level1['level1']
        print map.px_width
        print map.px_height
        self.level = scene.Scene(map)
        map.set_view(0, 0, 640, 480)
        manager = layer.ScrollingManager(director.window)
        manager.add(map, z = 1)
        manager.set_focus(256, 256)
        self.level.add(manager)
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
        #director.run(self.scenes["SPLASH"])
        director.run(self.scenes["GAME"])

engine = Engine()
