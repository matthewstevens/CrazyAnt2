''' Engine that handles the interaction of the game logic and the underlying libraries
Like the cocos2d director it is a singleton.
'''

import cocos
from cocos.director import director
from util_layers import HelloWorld, KeyDisplay, MouseDisplay

class Engine:
    def init(self):
        """
        Initialise the director, then load the levels
        Then create the scenes
        """
        cocos.director.director.init()
        self.scenes = []
    def run(self): 
        hello_layer = HelloWorld()
        main_scene = cocos.scene.Scene(hello_layer, KeyDisplay(), MouseDisplay())
        cocos.director.director.run(main_scene)

engine = Engine()
