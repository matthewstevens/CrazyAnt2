
import cocos
import cocos.actions as actions
import cocos.layer as layer
import cocos.menu as menu
from cocos.text import Label
from cocos.director import director
import pyglet

class HelloWorld(cocos.layer.ColorLayer):
    def __init__(self):
        super(HelloWorld, self).__init__(64, 64, 224, 255)
        label = cocos.text.Label('hello, world', font_name='Times New Roman', font_size=32, anchor_x='center', anchor_y='center')
        label.position = 320,240
        scale = actions.ScaleBy(3, duration=2)
        label.do(actions.Repeat(scale + actions.Reverse(scale)))
        self.add( label )

class KeyDisplay(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super(KeyDisplay, self).__init__()
        self.text = cocos.text.Label("", x=100, y = 280)

        self.keys_pressed = set()
        self.update_text()
        self.add(self.text)
    def update_text(self):
        key_names = [pyglet.window.key.symbol_string (k) for k in self.keys_pressed]
        text = 'Keys: '+','.join (key_names)
        # Update self.text
        self.text.element.text = text

    def on_key_press (self, key, modifiers):
        """This function is called when a key is pressed.
        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, capslock, etc.)
        """

        self.keys_pressed.add (key)
        self.update_text()

    def on_key_release (self, key, modifiers):
        """This function is called when a key is released.

        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, capslock, etc.)

        Constants are the ones from pyglet.window.key
        """

        self.keys_pressed.remove (key)
        self.update_text()

class MouseDisplay(cocos.layer.Layer):

    is_event_handler = True     #: enable pyglet's events

    def __init__(self):
        super( MouseDisplay, self ).__init__()

        self.posx = 100
        self.posy = 240
        self.text = cocos.text.Label('No mouse events yet', font_size=18, x=self.posx, y=self.posy )
        self.add( self.text )

    def update_text (self, x, y):
        text = 'Mouse @ %d,%d' % (x, y)
        self.text.element.text = text
        self.text.element.x = self.posx
        self.text.element.y = self.posy

    def on_mouse_motion (self, x, y, dx, dy):
        """This function is called when the mouse is moved over the app.

        (x, y) are the physical coordinates of the mouse
        (dx, dy) is the distance vector covered by the mouse pointer since the
            last call.
        """
        self.update_text (x, y)

    def on_mouse_press (self, x, y, buttons, modifiers):
        """This function is called when any mouse button is pressed

        (x, y) are the physical coordinates of the mouse
        'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise or of pyglet.window.key modifier constants
            (values like 'SHIFT', 'OPTION', 'ALT')
        """
        self.posx, self.posy = director.get_virtual_coordinates (x, y)
        self.update_text (x,y)

class GotoMenuScreen(actions.Action):
    def __init__(self, *args, **kargs):
        super(GotoMenuScreen, self).__init__(*args, **kargs)
    def start(self):
        from engine import engine
        engine.transition("MENU")
        
class SplashScreenLayer(layer.ColorLayer):
    def __init__(self):
        super(SplashScreenLayer, self).__init__(64, 64, 224, 255)
        self.label = Label('hello, world', font_name='Times New Roman', font_size=32, anchor_x='center', anchor_y='center')
        self.label.position = 320,240
        scale = actions.ScaleBy(3, duration=1)
        self.label.do(actions.Delay(1) + scale + actions.Reverse(scale) + GotoMenuScreen())
        self.add(self.label)
        

class MenuBackground(layer.ColorLayer):
    def __init__(self):
        super(MenuBackground, self).__init__(0, 0, 0, 255)

class MainMenu(menu.Menu):
    def __init__(self):
        #self.background = cocos.layer.ColorLayer(0, 0, 0, 255)
        super(MainMenu, self).__init__("Captured under thread")
        self.font_title['font_size'] = 42
        self.font_item['font_size'] = 32
        self.font_item_selected['font_size'] = 36
        self.menu_valign = menu.CENTER
        self.menu_halign = menu.CENTER
        self.create_menu([
            menu.MenuItem('New Game', self.on_new_game),
            menu.MenuItem('Options', self.on_options),
            menu.MenuItem('Quit', self.on_quit),
        ], menu.zoom_in(), menu.zoom_out())
        #self.scene = cocos.scene.Scene(self.background, self.menu)
    def on_new_game(self):
        print "ong"
    def on_options(self):
        print self.parent.switch_to(1)
    def on_quit(self):
        director.pop()

class OptionMenu(menu.Menu):
    def __init__(self):
        super(OptionMenu, self).__init__("Options")
        self.font_title['font_size'] = 42
        self.font_item['font_size'] = 32
        self.font_item_selected['font_size'] = 36
        self.menu_valign = menu.CENTER
        self.menu_halign = menu.CENTER
        self.create_menu([
            menu.MenuItem('Okay', self.on_okay),
        ], menu.zoom_in(), menu.zoom_out())
    def on_okay(self):
        self.parent.switch_to(0)
